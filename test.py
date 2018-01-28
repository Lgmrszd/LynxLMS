import dbconfig as LMS
from managers.group_manager import Group

LMS.init_db("localhost", "AdminsStrongPassword")
s = Group.select()
print(len(s))
