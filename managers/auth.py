import peewee as pw
import bcrypt
import random
import datetime
import json
import inspect
from db_connect import BaseModel

class Auth:
    """Class that manages authentication and authorization 
    """
    access_level = None #Access lelve of current user
    last_auth_time = None   #Last authentication time
    last_wrong_access_time = None
    delay_get_access = 30
    delay_auth = 30
    access_map = None   #Dictionary containing access map

    @classmethod
    def login(cls, login, password):
        """Login to the system using login and password
        """
        #Check if wrong authentication was recently
        current_time = datetime.datetime.today()
        if (not (cls.last_auth_time is None) and 
            (current_time - cls.last_auth_time).seconds < cls.delay_auth):
            cls.last_auth_time = current_time
            return -2
        #Get the user
        query = AuthUsers.select().where(AuthUsers.login == login)
        if (len(query) == 0):
            return -1
        #Check the password
        elif (len(query) == 1):
            entry = query.get()
            if (bcrypt.checkpw(str(password).encode(), entry.password.encode())):
                if (entry.auth_user_id == 1):
                    cls.access_level = ('admin', 99)
                    return 0
                else:
                    cls.access_level = ('librarian', entry.privilege)
                    return 0
            return -1
        else:
            print('Houston, problem in auth.Auth.authentication')
            return -1

    @classmethod
    def load_access_map(cls):   #TODO : Exceptions
        """Load access map. It describes modules and their attributes that require authorization
        """
        if cls.access_map is None:
            access_map_file = './data/access_map.json'
            with open(access_map_file, 'r') as json_file:
                cls.access_map = json.load(json_file)

    @classmethod
    def get_access(cls, module, name):
        """Returns true if user has permissions to use specific method
        """
        current_time = datetime.datetime.today()
        #if last wrong get_access was less than some seconds (delay) ago then refuse
        if (cls.last_wrong_access_time != None and \
            (current_time - cls.last_wrong_access_time).seconds < cls.delay_get_access):
            cls.last_wrong_access_time = current_time
            return False
        if not (cls.access_level is None):
            #check if user can use certain method here 
            #Check if access map is initialized
            cls.load_access_map()
            if name in cls.access_map[module].keys():
                allowed = cls.access_map[module][name]  #Get minimum privileges which allow user to perform operation 
            else:
                return True #Method is not in access map
            if cls.access_level[0] is 'admin':  #Check privilege for admin
                return True
            if cls.access_level[0] is 'librarian':  #Check privilege for librarian
                if allowed <= cls.access_level[1]:
                    return True
            return False
        cls.last_wrong_access_time = current_time
        return False
    
    @classmethod
    def log_out(cls):
        """Log out from the system
        """
        if cls.access_level is None:
            return False
        cls.access_level = None
        return True

def require_auth(cls, func):
    """Decorator that checks if user has permissions to use this method
    """
    def wrapper(*args, **kwargs):
        if (Auth.get_access(cls.__name__, func.__name__)):
            return func(*args, **kwargs) 
        return None
    return wrapper

def require_auth_class():
    """Class decorator, that decorate methods described in access map
    """
    def decorate(cls):
        #for attrib in cls.__dict__:
        for name, funct in inspect.getmembers(cls):
            #funct = getattr(cls, attrib)
            if Auth.access_map is None:
                Auth.load_access_map()
            if ((inspect.isfunction(funct) or inspect.ismethod(funct)) and 
                name in Auth.access_map[cls.__name__].keys()):
                setattr(cls, name, require_auth(cls, funct))
            #if inspect.isfunction(funct) or inspect.ismethod(funct):
            #    setattr(cls, name, require_auth(cls, funct))
        return cls
    return decorate

class AuthUsers (BaseModel):
    """Class that manages users who need authentication
    """
    auth_user_id = pw.PrimaryKeyField()
    login = pw.CharField(unique=True)
    password = pw.CharField()
    privilege = pw.SmallIntegerField()
    info = pw.CharField()
    last_wrong_access_time = None
    admin_delay = 30

    @classmethod
    def admin_check(cls, login, password):
        """Check administrator's credentials
        """
        query = cls.select().where(cls.auth_user_id == 1)
        current_time = datetime.datetime.today()
        if (not (cls.last_wrong_access_time is None) and \
            (current_time - cls.last_wrong_access_time).seconds < cls.admin_delay):
            return False
        if (len(query) == 0):
            print('Houston, we have problems. admin_check in auth')
            return False
        admin_info = query.get()
        if (admin_info.login == login and bcrypt.checkpw(str(password).encode(), admin_info.password.encode())):
            return True
        return False

    @classmethod
    def add(cls, admin, login, password, privilege, info):
        """Add librarian with specific privileges
        """
        if (cls.admin_check(admin[0], admin[1])):
            if (privilege < 0 or privilege > 3):
                return 1
            hashed = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
            AuthUsers.create(login=login, password=hashed, privilege=privilege, info=info)
            return 0
        else:
            return 1
    
    @classmethod
    def remove(cls, admin, auth_user_id):
        """Remove librarian with specific ID
        """
        if (auth_user_id == 1):
            return 3
        if (cls.admin_check(admin[0], admin[1])):
            query = cls.select().where(cls.auth_user_id == auth_user_id)
            if (len(query) == 1):
                query.get().delete_instance()
                return 0
            elif (len(query) == 0):
                return 2
            elif (len(query) > 1):
                print('Houston, huge problems. auth.AuthUsers.remove')
                return 1
        else:
            return 1

    @classmethod
    def get_list(cls, admin):
        """Get the list of all users
        """
        if (cls.admin_check(admin[0], admin[1])):
            query = cls.select(cls.auth_user_id, cls.login, cls.privilege, cls.info)
            res = list(query)
            return (0,res)
        return (1, None)