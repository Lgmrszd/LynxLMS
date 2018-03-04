import peewee as pw
from db_connect import BaseModel
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import managers.doc_manager as doc_manager
import datetime


class History(BaseModel):
    """Data model for all checkout and return operations
    """
    OperationID = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(user_manager.User, related_name = 'operations')
    copy = pw.ForeignKeyField(doc_manager.Copy, related_name = 'operations')
    librarian_co = pw.CharField()
    date_check_out = pw.DateField(formats = '%Y-%m-%d')
    librarian_re = pw.CharField(null = True)
    date_return = pw.DateField(formats = '%Y-%m-%d', null = True)


class Booking_system:
    """Booking system class
    """
    __fine = 100

    def check_out(self, user, copy, librarian):
        """Check out copy of specific document to specific user
        """
        if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
            return (4, None)
        if copy.active == False:
            return (3, None)
        if 'reference' in copy.get_doc().keywords:
            return (2, None)
        if copy.checked_out == True:
            return (1, None)
        #Check if user checked out another copy of this document
        copy_doc = copy.get_doc()
        for entry in self.get_user_history(user):
            if (entry.date_return == None and entry.copy.get_doc() == copy_doc):
                return (6, None)
        current_date = datetime.date.today()
        res = History.create(user = user, copy = copy, librarian_co = librarian, date_check_out = current_date)
        copy.checked_out = True
        copy.save()
        return (0, res)
    
    def return_by_entry(self, entry, librarian):
        """Return copy by "History" entry
        """
        if (entry.date_return != None):
            return 1
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = librarian
        entry.save()
        entry.copy.checked_out = False
        entry.copy.save()
        entry.user.fine += self.check_overdue(entry)
        entry.user.save()
        return 0
        
    
    def return_by_copy(self, copy, librarian):
        """Return copy
        """
        query = History.select().where((History.date_return.is_null(True)) &  (History.copy == copy))
        if (len(query) == 0):
            return 3
        if (len(query) > 1):
            return 2
        entry = query.get()
        return self.return_by_entry(entry, librarian)

    def get_list(self, rows_number, page, opened=0):
        """Returns a content from certain page of history check out
        Overdue opened=2, Opened - opened=1, All - opened=0, Closed - opened=-1
        """
        res = []
        select_query = None
        if (opened == 0):
            select_query = History.select()
        elif (opened == 1):
            select_query = History.select().where(History.date_return.is_null(True))
        elif (opened == 2):
            select_query = History.select().where(History.date_return.is_null(True))
            overdue_entries = []
            for entry in select_query:
                if (self.check_overdue(entry) > 0):
                    overdue_entries.append(entry)
            page_number = len(overdue_entries) // rows_number
            if (len(overdue_entries) % rows_number > 0):
                page_number += 1
            return (overdue_entries[(page-1) * rows_number : page * rows_number], page_number)
        elif (opened == -1):
            select_query = History.select().where(History.date_return.is_null(False))
        else:
            return ([], 0)
        #Calculating number of pages
        page_number = int(select_query.count()) // rows_number
        if (select_query.count() % rows_number > 0):
            page_number += 1
        query = select_query.offset(0 + (page-1)*rows_number).limit(rows_number)
        for entry in query:
            res.append(entry)
        return res, page_number

    def get_user_history(self, user):
        """Get all operation for particular user
        """
        query = user.operations
        res = []
        for entry in query:
            res.append(entry)
        return res
    
    def get_copy_history(self, copy):
        """Get all operations for particular copy
        """
        query = copy.operations
        res = []
        for entry in query:
            res.append(entry)
        return res
    
    def get_document_copies(self, doc):
        """Get list of copies of speciific document
        """
        return doc.get_document_copies()

    def get_max_return_time(self, entry):
        """Returns maximum copy return time by history entry
        """
        date_splitted = entry.date_check_out.split('-')
        date_check_out = datetime.date(int(date_splitted[0]),
                                       int(date_splitted[1]),
                                       int(date_splitted[2]))
        user = entry.user
        date_return = date_check_out + datetime.timedelta(
            days=7 * user.group.get_checkout_time(entry.copy.get_doc())
        )
        return str(date_return)

    def check_overdue(self, entry):
        """Returns fine for overdue (0 if no fine)
        """
        period = 7 * 2
        if ((type(entry.copy.get_doc()) == doc_manager.name_to_class()['Book']) and ('best seller' in entry.copy.get_doc().keywords)):
            period = entry.user.group.book_bestseller_ct * 7
        else:
            period = entry.user.group.get_checkout_time(entry.copy.get_doc())
        date_return = entry.date_return
        if (date_return == None):   #if we are trying to check open entry
            date_return = str(datetime.date.today())
        res = min(self.overdue(entry.date_check_out, date_return, period), entry.copy.get_doc().cost)
        return res

    def overdue(self, date_check_out, date_return, period):
        """Calculates fine
        """
        d1_l = date_return.split('-')
        d2_l = date_check_out.split('-')
        d1 = datetime.date(int(d1_l[0]), int(d1_l[1]), int(d1_l[2]))
        d2 = datetime.date(int(d2_l[0]), int(d2_l[1]), int(d2_l[2]))
        res = max((d1 - d2).days - period, 0) * self.__fine
        return res
    
    def pay_fine(self, usr, amount):
        """Pay fine of specific user.
        Returns change
        """
        usr.fine = max(usr.fine - amount, 0)
        return (max(amount - usr.fine, 0))
