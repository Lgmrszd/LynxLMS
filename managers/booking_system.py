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

class Queue(BaseModel):
    """Data model for document queue
    """
    QueueID = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(user_manager.User, related_name='queue')
    priority = pw.SmallIntegerField()
    docClass = pw.CharField()
    docId = pw.IntegerField()
    assigned_copy = pw.ForeignKeyField(doc_manager.Copy, related_name='reserved', null=True)
    time_out = pw.DateField(formats='%Y-%m-%d', null=True)
    active = pw.BooleanField(default=True) #if user is in queue    
    
    @classmethod
    def push_to_queue(cls, doc, user):
        """Pushes user to queue for specific document
        """
        #TODO : FIX PRIORITY!!!!!!!1111111
        #Check if user is already in queue
        docClass = doc_manager.class_to_name()[type(doc)]
        docId = doc.DocumentID
        select_query = Queue.select().where(Queue.user == user, Queue.active == True,
                                            Queue.docClass == docClass,
                                            Queue.docId == docId)
        if (len(select_query) == 1):
            return None
        elif (len(select_query) > 1):
            print('Houston, we have a problem in booking system in push_to_queue')
            return None
        
        return Queue.create(docClass=docClass, docId=docId , user=user, priority = 1)
    
    @classmethod
    def remove_from_queue(cls, doc):
        """Removes user from queue
        """
        #res = self.get_from_queue(doc)
        #Queue.delete().where(Queue.docClass == doc_manager.class_to_name()[type(doc)],
        #                     Queue.docId == doc.DocumentID,
        #                     Queue.active == True, Queue.user == res).execute()
        entry = cls.get_queue_entry(doc)
        if (entry == None):
            return None
        res = entry.user
        entry.delete_instance()
        return res
    
    @classmethod
    def get_queue_entry(cls, doc):
        """Gets entry from queue.
           If active = 1 then it returns entry with not assigned copy
           If active = 0 then it returns entry with out assigned copy
        """
        #Find earliest with higher prority
        select_query = Queue.select(Queue.priority).where(Queue.docClass == doc_manager.class_to_name()[type(doc)],
                                                    Queue.docId == doc.DocumentID, Queue.active == True).distinct()
        #if queue is empty
        if (len(select_query) == 0):
            return None
        #Find max priority
        max_priority = -1
        for entry in select_query:
            if (entry.priority > max_priority): #possible bug due to no entries
                max_priority = entry.priority
        
        print(max_priority)

        docClass = doc_manager.class_to_name()[type(doc)]
        docId = doc.DocumentID

        entry = Queue.select().where(Queue.docClass == docClass, Queue.docId == docId,
                               Queue.priority == max_priority, Queue.active == True).get() #check if return least id
        #TODO : Try to optimize
        return entry
    
    @classmethod
    def get_user_from_queue(cls, copy): #TODO : change copy to document!
        doc = copy.get_doc()
        res = cls.get_queue_entry(doc)
        if (res == None):
            return None
        current_date = datetime.date.today()
        res.time_out = str(current_date)
        res.assigned_copy = copy
        res.active = False
        res.save()
        copy.checked_out = 1
        copy.save()
        return res.user
    
    @classmethod
    def update_queue(cls):
        select_query = Queue.select().where(Queue.active == False)
        current_date = datetime.date.today()
        users = []
        for entry in select_query:
            time_out_date = datetime.datetime.strptime(entry.time_out,'%Y-%m-%d')
            if (current_date >= time_out_date):
                #inform user here
                users.append(entry.user)
                copy = entry.assigned_copy 
                if (cls.get_user_from_queue(copy) == None):
                    copy.checked_out = 0
                    copy.save()
                entry.delete_instance()
        return users
    
    @classmethod
    def red_button(cls, doc):
        docClass = doc_manager.class_to_name()[type(doc)]
        docId = doc.DocumentID
        select_query = Queue.select().where(Queue.docClass == docClass, Queue.docId == docId)
        users = []
        #TODO : Replace code below with 2-3 queries!!!
        for entry in select_query:
            users.append(entry.user) #inform user
            entry.delete_instance()
        copies = doc.get_document_copies()
        for copy in copies:
            if (copy.checked_out == 1):
                copy.check_out = 0
                copy.save()


class Booking_system:
    """Booking system class
    """
    __fine = 100

    def check_out_old(self, user, copy, librarian): #TODO : Check out by document
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
            return (6, None) #Already in the queue
        return (1, None)
    
    def check_out_reserved(self, doc, user, librarian): #TODO : Add user to args. Rework remove from queue!!!
        """Checks out reserved copy of document
        """
        #TODO : Find entry in queue with specific user and
        
        docClass = doc_manager.class_to_name()[type(doc)]
        docId = doc.DocumentID
        ent = Queue.select().where(Queue.user == user,
                                   Queue.docClass == docClass, Queue.docId == docId,
                                   Queue.active == False)
        
        if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
            return (4, None)
        if doc.active == False:
            return (3, None)
        if 'reference' in doc.keywords:
            return (2, None)
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


        # ##!
        # copies = doc.get_document_copies()
        # for copy in copies:
        #     if (copy.checked_out == 1):
        #         user = self.remove_from_queue(doc)

        #         if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
        #             return (4, None)
        #         if doc.active == False:
        #             return (3, None)
        #         if 'reference' in doc.keywords:
        #             return (2, None)
                
        #         #it is not possible that user already has copy, but just to ensure
        #         for entry in self.get_user_history(user):
        #             if (entry.date_return == None and entry.copy.get_doc() == doc):
        #                 return (6, None)
                
        #         copy.check_out = 2
        #         copy.save()
        #         current_date = datetime.date.today()
        #         res = History.create(user=user, copy=copy, librarian_co=librarian, date_check_out=current_date)
        #         return(0, res)
        
        #return(1, None) #Nothing to check out
    

    #TODO : ADD GET FROM QUEUE AND ASSIGN TO THIS USER
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
        queue_next = Queue.get_user_from_queue(entry.copy)
        if queue_next == None:
            return 0
        #Inform user about free copy here <-
        return 2 #assigned to someone in the queue
        
        
    
    #TODO : ADD GET FROM QUEUE AND ASSIGN TO THIS USER
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
        date_return = None
        if ((type(entry.copy.get_doc()) == doc_manager.name_to_class()['Book']) and ('best seller' in entry.copy.get_doc().keywords)):
            date_return = date_check_out + datetime.timedelta(
                days=7 * user.group.book_bestseller_ct
            )
        else:
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
            period = entry.user.group.get_checkout_time(entry.copy.get_doc()) * 7
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
