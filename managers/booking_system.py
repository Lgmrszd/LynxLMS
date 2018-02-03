import peewee as pw
from db_connect import BaseModel
import managers.user_manager as user_manager
import managers.doc_manager as doc_manager
import datetime


class History(BaseModel):
    OperationID = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(user_manager.User, related_name = 'operations')
    copy = pw.ForeignKeyField(doc_manager.Copy, related_name = 'operations')
    librarian_co = pw.CharField()
    date_check_out = pw.DateField(formats = '%Y-%m-%d')
    librarian_re = pw.CharField(null = True)
    date_return = pw.DateField(formats = '%Y-%m-%d', null = True)


class Booking_system:
    def check_out(self, user, copy, librarian):
        if copy.checked_out == True:
            return 0
        current_date = datetime.date.today()
        res = History.create(user = user, copy = copy, librarian_co = librarian, date_check_out = current_date)
        copy.checked_out = True
        copy.save()
        return res
    
    def return_by_entry(self, entry, librarian):
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = librarian
        entry.save()
        entry.copy.checked_out = False
        entry.copy.save()
    
    def return_by_copy(self, copy, librarian):
        current_date = datetime.date.today()
        entry = History.select().where(History.date_return.is_null(True) & History.copy == copy).get()
        entry.date_return = str(current_date)
        entry.librarian_re = librarian
        entry.save()
        copy.checked_out = False
        copy.save()

    
    def get_list_overdue(self):
        query = History.select().where(History.date_return.is_null(True))
        res = []
        for entry in query:
            res.append(entry)
        return res

    def get_user_history(self, user):
        query = user.operations
        res = []
        for entry in query:
            res.append(entry)
        return res
    
    def get_copy_history(self, copy):
        query = copy.operations
        res = []
        for entry in query:
            res.append(entry)
        return res
