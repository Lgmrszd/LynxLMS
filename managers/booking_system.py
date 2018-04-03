import peewee as pw
from db_connect import BaseModel
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import managers.doc_manager as doc_manager
import datetime
from managers.user_manager import Queue as Queue
from managers.user_manager import Request as Request
import managers.notifier


class History(BaseModel):
    """Data model for all checkout and return operations
    """
    OperationID = pw.PrimaryKeyField()
    renewed = pw.BooleanField(default=False)
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
    
    def check_out(self, doc, user, librarian):
        """Check outs copy by document and user entries. If there is no available copy, user is placed in queue
        """
        if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
            return (4, None)
        if doc.active == False:
            return (3, None)
        if 'reference' in doc.keywords:
            return (2, None)

        for entry in self.get_user_history(user):
            if (entry.date_return == None and entry.copy.get_doc() == doc):
                return (6, None)
        
        #Check if copy reserved. If it is not reserved, method check_out_reserved returns error
        #and checks out document otherwise
        reserved = self.__check_out_reserved(doc, user, librarian)
        if (reserved[0] == 0):
            return reserved

        #find copy that is not checked out
        #TODO : replace with one query
        copies = doc.get_document_copies()
        for entry in copies:
            if (entry.checked_out == 0):
                entry.checked_out = 2
                entry.save()
                current_date = datetime.date.today()
                res = History.create(user = user, copy = entry, librarian_co = librarian, date_check_out = current_date)
                return (0, res)
        res = Queue.push_to_queue(doc, user)
        if (res == None):
            return (7, None) #Already in the queue
        return (1, None)
    
    def __check_out_reserved(self, doc, user, librarian):
        """Checks out reserved copy of document
        """
        docClass = doc_manager.class_to_name()[type(doc)]
        docId = doc.DocumentID
        ent = Queue.select().where(Queue.user == user,
                                   Queue.docClass == docClass, Queue.docId == docId,
                                   Queue.active == False)
        
        # if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
        #     return (4, None)
        # if doc.active == False:
        #     return (3, None)
        # if 'reference' in doc.keywords:
        #     return (2, None)
        if (len(ent) == 0):
            return (1, None) #Nothing to check out
        if (len(ent) > 1):
            print('Houston, we have a problem in booking system in check_out_reserved')
            return (1, None)

        ent = ent.get()
        copy = ent.assigned_copy
        copy.checked_out = 2
        copy.save()
        current_date = datetime.date.today()
        res = History.create(user=user, copy=copy, librarian_co=librarian, date_check_out=current_date)
        ent.delete_instance()
        return(0, res)
    

    def return_by_entry(self, entry, librarian):
        """Return copy by "History" entry
        """
        if (entry.date_return != None):
            return 1
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = librarian
        entry.save()
        entry.copy.checked_out = 0
        entry.copy.save()
        entry.user.fine += self.check_overdue(entry)
        entry.user.save()
        if (entry.copy.get_doc().requested == True):
            doc = entry.copy.get_doc()
            user = Request.get_user(doc)
            self.check_out(doc, user, librarian)
            Request.close_request(user, doc, librarian)
            return 5
        queue_next = Queue.get_user_from_queue(entry.copy)
        if queue_next == None:
            return 0
        #Inform user about free copy here <-
        text = "Dear %s,\nQueued document \"%s\" for you is ready.\n"\
               % (queue_next.name + " " + queue_next.surname, entry.copy.get_doc().title)
        managers.notifier.send_message(entry.user.email, "Document queue abandoned", text)
        return 4 #assigned to someone in the queue
        
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
    
    def renew_by_entry(self, entry, librarian):
        """Renew copy for certain user using History entry"""
        if (entry.date_return != None):
            return(1, None)
        if (self.check_overdue(entry) != 0):
            return(2, None)
        if (entry.copy.get_doc().requested == True):
            return(3, None)
        if (entry.renewed == True):
            return(6, None)
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = librarian
        entry.save()
        res = History.create(user=entry.user, copy=entry.copy, librarian_co=librarian, 
                             date_check_out=current_date, renewed=True)
        return(0, res)

    def renew_by_copy(self, copy, librarian):
        """Renew by copy"""
        query = History.select().where((History.date_return.is_null(True)) &  (History.copy == copy))
        if (len(query) == 0):
            return (4, None)
        if (len(query) > 1):
            return (5, None)
        entry = query.get()
        return self.renew_by_entry(entry, librarian)
    
    def __outstanding_request_old(self, doc, users, librarian):
        """Places outstanding request for certain document for list of users.
        Returns (code, list of 'check outs' if there were free copies after removing queue, waiting list)"""
        #Check if there is available copy
        copies = doc.get_document_copies()
        available_copies = []
        #TODO : replace the following loop with one query
        for copy in copies:
            if (copy.checked_out == 0):
                available_copies.append(copy)
        if (len(available_copies) > 0):
            return (1, None, None)
        Queue.red_button(doc)
        copies = doc.get_document_copies()  #update copies
        user_idx = 0
        received_copies = []    #List of users, who received copies after this method executed
        waiting_copies = []     #List of users, who are waiting for copies
        #if we have free copies after deleting queue, check out to users who are in request
        for copy in copies:
            if (copy.checked_out == 0):
                received_copies.append(self.check_out(doc, users[user_idx], librarian))
                user_idx += 1
                if (user_idx == len(users)): 
                    break
        #Placing requests
        users = users[user_idx:]
        for user in users:
            waiting_copies.append(Request.place_request(doc, user, librarian))
        return (0, received_copies, waiting_copies)

    def outstanding_request(self, doc, user, librarian):
        """Places outstanding request for certain document for list of users.
        Returns (code, history entry (if there was free copy after queue abandon) or request entry)"""
        #If any request for this document exists, cancel it
        entry = Request.get_user(doc)
        if (entry != None):
            entry.active = False
            entry.save()
            if (Request.get_user(doc) != None):
                print('Houston, we have a problems. Outstanding request, booking system')
        #Check if there is available copy
        copies = doc.get_document_copies()
        for copy in copies:
            if (copy.checked_out == 0):
                return(2, None)
        Queue.red_button(doc)
        copies = doc.get_document_copies()  #update copies
        #if we have free copies after deleting queue, check out to users who are in request
        for copy in copies:
            if (copy.checked_out == 0):
                res = self.check_out(doc, user,librarian)
                return(1, res)
        #Placing requests
        res = Request.place_request(doc, user, librarian)
        return (0, res)
    
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
        doc = entry.copy.get_doc()
        date_return = None

        period = 7 * 2 #Some default period
        if (entry.renewed == False):
            period = user.group.get_checkout_time(doc) * 7
        else:
            period = user.group.get_renew_time(doc) * 7
        
        date_return = date_check_out + datetime.timedelta(days=period)
        return str(date_return)

    def check_overdue(self, entry):
        """Returns fine for overdue (0 if no fine)
        """
        period = 7 * 2 #Some default period
        doc = entry.copy.get_doc()
        if (entry.renewed == False):
            period = entry.user.group.get_checkout_time(doc) * 7
        else:
            period = entry.user.group.get_renew_time(doc) * 7
        date_return = entry.date_return
        if (date_return == None):   #if we are trying to check open entry
            date_return = str(datetime.date.today())
        res = min(self.overdue(entry.date_check_out, date_return, period), entry.copy.get_doc().cost)
        return res

    def overdue(self, date_check_out, date_return, period):
        """Calculates fine
        """
        date_return_d = datetime.datetime.strptime(date_return, '%Y-%m-%d')
        date_check_out_d = datetime.datetime.strptime(date_check_out, '%Y-%m-%d')
        res = max((date_return_d - date_check_out_d).days - period, 0) * self.__fine
        return res
    
    def pay_fine(self, usr, amount):
        """Pay fine of specific user.
        Returns change
        """
        usr.fine = max(usr.fine - amount, 0)
        return (max(amount - usr.fine, 0))
