from dbconnect import LMSDB

db = LMSDB("postgres://admin:AdminsStrongPassword@localhost:5432/LynxLMS")
db.close()