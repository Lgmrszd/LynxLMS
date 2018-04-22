import managers.doc_manager
import managers.user_manager
import managers.group_manager
import managers.booking_system
import managers.auth
import bcrypt
from db_connect import db
from os import path, makedirs


def init_db(db_filename="./data/database.db"):
    dirname, _ = path.split(db_filename)
    if dirname != "" and not path.exists(dirname):
        makedirs(dirname)
    db.init(db_filename)
    db.connect()
    create_tables()


def create_tables():
    # Creating tables
    db.create_tables([managers.doc_manager.Book,
                      managers.doc_manager.AVMaterial,
                      managers.doc_manager.JournalArticle,
                      managers.doc_manager.Copy,
                      managers.user_manager.User,
                      managers.group_manager.Group,
                      managers.booking_system.History,
                      managers.user_manager.Queue,
                      managers.user_manager.Request,
                      managers.auth.AuthUsers], safe=True)
    #deleted_group = managers.group_manager.Group.get(managers.group_manager.Group.name == 'Deleted')
    deleted_group = len(managers.group_manager.Group.select().where(managers.group_manager.Group.name == 'Deleted'))
    if (deleted_group == 0):
        managers.group_manager.Group.create(name='Deleted', book_ct=-1, book_bestseller_ct=-1, journal_ct=-1, av_ct=-1,
                                            book_rt=-1, book_bestseller_rt=-1, journal_rt=-1, av_rt=-1, priority=-1)

    students_group = len(managers.group_manager.Group.select().where(managers.group_manager.Group.name == 'Students'))
    if (students_group == 0):
        managers.group_manager.Group.create(name='Students', book_ct=3, book_bestseller_ct=2, journal_ct=2, av_ct=2,
                                        book_rt=3, book_bestseller_rt=2, journal_rt=2, av_rt=2, priority=0)

    faculty_group = len(managers.group_manager.Group.select().where(managers.group_manager.Group.name == 'Faculty'))
    if (faculty_group == 0):
        managers.group_manager.Group.create(name='Faculty', book_ct=4, book_bestseller_ct=4, journal_ct=2, av_ct=2,
                                        book_rt=4, book_bestseller_rt=4, journal_rt=2, av_rt=2, priority=2)

    vp_group = len(managers.group_manager.Group.select().where(managers.group_manager.Group.name == 'Visiting professors'))
    if (vp_group == 0):
        managers.group_manager.Group.create(name='Visiting professors', book_ct=1, book_bestseller_ct=1, journal_ct=1, av_ct=1,
                                        book_rt=1, book_bestseller_rt=1, journal_rt=1, av_rt=1, priority=1)
    if (managers.auth.AuthUsers.select().count() == 0):
        admin_login = 'admin'   #TODO: replace this code somehow
        admin_pass = bcrypt.hashpw('pass'.encode(), bcrypt.gensalt())
        managers.auth.AuthUsers.create(login=admin_login, password=admin_pass, privilege=99, info='Temporary admin account. \
                                        If you see this entry in database, report to developers, please')

def drop_tables():
    db.drop_tables([managers.doc_manager.Book,
                    managers.doc_manager.AVMaterial,
                    managers.doc_manager.JournalArticle,
                    managers.doc_manager.Copy,
                    managers.user_manager.User,
                    managers.group_manager.Group,
                    managers.booking_system.History,
                    managers.user_manager.Queue,
                    managers.user_manager.Request,
                    managers.auth.AuthUsers], safe=True) #It removes AuthUsers!!!

