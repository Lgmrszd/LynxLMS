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
    __fine = 100

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
        entry.user.fine += self.check_overdue(entry)
        entry.user.save()
        
    
    def return_by_copy(self, copy, librarian):
        entry = History.select().where(History.date_return.is_null(True) & History.copy == copy).get()
        self.return_by_entry(entry, librarian)

    
    def get_list_overdue(self):
        opened = self.get_list_opened()
        res = []
        for entry in opened:
            if (self.check_overdue(entry) > 0):
                res.append(entry)
        return res

    def get_list_opened(self):
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
    
    def get_document_copies(self, doc):
        doc_class = doc_manager.class_to_name()[type(doc)]
        query = doc_manager.Copy.select().where(doc_manager.Copy.docClass == doc_class , doc_manager.Copy.docId == doc.DocumentID)
        #print('::: doc_class = ' + doc_class + ' ::: docId = ' + str(doc.DocumentID) + '\n')
        res = [] 
        for entry in query:
            res.append(entry)
        return res

    def check_overdue(self, entry):
        period = 7 * 2
        if (type(entry.doc) == doc_manager.name_to_class()['AVMaterial']):
            period = entry.user.group.av_ct * 7
        elif (type(entry.doc) == doc_manager.name_to_class()['Book']):
            if (entry.doc.keywords == 'best seller'):
                period = entry.user.group.book_bestseller_ct * 7
            else:
                period = entry.user.group.book_ct * 7
        elif (type(entry.doc) == doc_manager.name_to_class()['JournalArticle']):
            period = entry.user.group.journal_ct * 7
        res = self.overdue(entry.date_check_out, entry.date_return, period)
        return res

    def overdue(self, date_check_out, date_return, period):
        d1_l = date_return.split('-')
        d2_l = date_check_out.split('-')
        d1 = datetime.date(int(d1_l[0]), int(d1_l[1]), int(d1_l[2]))
        d2 = datetime.date(int(d2_l[0]), int(d2_l[1]), int(d2_l[2]))
        res = max((d1 - d2).days - period, 0) * self.__fine
        return res