import datetime
import logging
import peewee as pw
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import managers.doc_manager as doc_manager
import managers.notifier
import managers.event_manager as event_manager
from db_connect import BaseModel
from managers.user_manager import Queue as Queue
from managers.user_manager import Request as Request
from managers.auth import require_auth_class


class History(BaseModel):
    """Data model for all checkout and return operations
    """
    OperationID = pw.PrimaryKeyField()
    renewed = pw.BooleanField(default=False)
    user = pw.ForeignKeyField(user_manager.User, related_name='operations')
    copy = pw.ForeignKeyField(doc_manager.Copy, related_name='operations')
    librarian_co = pw.CharField()
    date_check_out = pw.DateField(formats='%Y-%m-%d')
    librarian_re = pw.CharField(null=True)
    date_return = pw.DateField(formats='%Y-%m-%d', null=True)


@require_auth_class()
class Booking_system:
    """Booking system class
    """
    __fine = 100  # Fine for the one day of overdue

    def __init__(self, librarian):
        self.librarian = librarian
        #Adding listener to proceed free copies via event_manager
        event_manager.register_listener('free_copy', self.proceed_free_copy)

    def check_out(self, doc, user):
        """Check outs copy by document and user entries. If there is no available copy, user is placed in queue
        """
        if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
            return (4, None)  # User is deleted
        if doc.active == False:
            return (3, None)  # Inactive document
        if 'reference' in doc.keywords:
            return (2, None)  # Document is reference

        for entry in self.get_user_history(user):
            if (entry.date_return == None and entry.copy.get_doc() == doc):
                return (6, None)  # User has a copy of this document

        # Check if copy reserved. If it is not reserved, method check_out_reserved returns error
        # and checks out document otherwise
        reserved = self._check_out_reserved(doc, user)
        if (reserved[0] == 0):
            return reserved

        # find copy that is not checked out
        copy_query = doc_manager.Copy.select().where(doc_manager.Copy.active == True,
                                                     doc_manager.Copy.checked_out == 0)
        if (len(copy_query) != 0):
            copy = copy_query.get()
            copy.checked_out = 2
            copy.save()
            current_date = datetime.date.today()
            res = History.create(
                user=user, copy=copy, librarian_co=self.librarian, date_check_out=current_date)
            return (0, res)  # successfully checked out

        # Push to the queue if there is no free copy
        res = Queue.push_to_queue(doc, user)
        if (res == None):
            return (7, None)  # Already is in the queue
        return (1, None)  # Placed in the queue

    def _check_out_reserved(self, doc, user):
        """Checks out reserved copy of document (Supposed to be called only from check_out method)
        """
        # Get Queue entry and check out assigned copy
        entry = Queue.get_to_remove(doc, user)
        if (entry == None):
            return (1, None)
        copy = entry.assigned_copy
        copy.checked_out = 2
        copy.save()
        current_date = datetime.date.today()
        res = History.create(
            user=user, copy=copy, librarian_co=self.librarian, date_check_out=current_date)
        entry.delete_instance()  # Delete entry after check out
        return (0, res)  # successfully checked out

    def return_by_entry(self, entry):
        """Return copy by "History" entry
        """
        if (entry.date_return != None):
            return 1  # Copy is already returned
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = self.librarian
        entry.save()
        entry.copy.checked_out = 0
        entry.copy.save()
        entry.user.fine += self.check_overdue(entry)
        entry.user.save()
        copy = doc_manager.Copy.get_by_id(entry.copy.CopyID)
        return self.proceed_free_copy(copy)

    def proceed_free_copy(self, copy):
        """Proceed free copy. Assign to people in the queue or check out if it is requested
        """
        if (copy.get_doc().requested == True):
            doc = copy.get_doc()
            user = Request.get_user(doc)
            self.check_out(doc, user)
            Request.close_request(user, doc)
            return 5  # Checked out to user in outstanding request
        queue_next = Queue.get_user_from_queue(copy)
        if queue_next == None:
            return 0  # Successfully returned
        # Inform user about free copy here <-
        # text = "Dear %s,\nQueued document \"%s\" for you is ready.\n" \
        #        % (queue_next.name + " " + queue_next.surname, copy.get_doc().title)
        # managers.notifier.send_message(
        #     queue_next.email, "Document is ready", text)
        managers.notifier.notify_free_copy([queue_next], copy.get_doc())
        return 4  # Assigned to someone in the queue

    def return_by_copy(self, copy):
        """Return copy
        """
        query = History.select().where(
            (History.date_return.is_null(True)) & (History.copy == copy))
        if (len(query) == 0):
            return 3  # No entry found
        if (len(query) > 1):
            #print('Houston, we have a problems. Return_by_copy, booking system')
            logging.error(
                'booking_system.Booking_system.return_by_copy(), copy is checked out to 2 or more users at the same time!')
            return 2  # Internal error
        entry = query.get()
        return self.return_by_entry(entry)

    def renew_by_entry(self, entry):
        """Renew copy for certain user using History entry"""
        if (entry.date_return != None):
            return (1, None)  # Copy is already returned
        if (self.check_overdue(entry) != 0):
            return (2, None)  # Copy is overdued
        if (entry.copy.get_doc().requested == True):
            return (3, None)  # Document is under outstanding request
        if (entry.renewed == True):  # TODO: check if copy is deleted
            return (6, None)  # Copy has been already renewed
        current_date = datetime.date.today()
        entry.date_return = str(current_date)
        entry.librarian_re = self.librarian
        entry.save()
        res = History.create(user=entry.user, copy=entry.copy, librarian_co=self.librarian,
                             date_check_out=current_date, renewed=True)
        return (0, res)

    def renew_by_copy(self, copy):
        """Renew by copy"""
        query = History.select().where(
            (History.date_return.is_null(True)) & (History.copy == copy))
        if (len(query) == 0):
            return (4, None)  # Copy is not checked out
        if (len(query) > 1):
            return (5, None)  # Internal error
        entry = query.get()
        return self.renew_by_entry(entry)

    def outstanding_request(self, doc, user):
        """Places outstanding request for certain document for list of users.
        Returns (code, history entry (if there was free copy after queue abandon) or request entry)"""
        if (user.group == group_manager.Group.get(group_manager.Group.name == 'Deleted')):
            return 4  # User is deleted
        if doc.active == False:
            return 3  # Document is inactive
        if 'reference' in doc.keywords:
            return 2  # Document is reference

        for entry in user.operations:
            if (entry.date_return == None and entry.copy.get_doc() == doc):
                return 6  # User already has copy of this document

        # If any request for this document exists, cancel it
        entry = Request.get_user(doc)
        if (entry != None):
            entry.active = False
            entry.save()
            if (Request.get_user(doc) != None):
                #print('Houston, we have a problems. Outstanding request, booking system')
                logging.error(
                    'booking_system.Booking_system.outstanding_request(), 2 users in outstanding request')
        # Check if there is available copy
        copies = doc.get_document_copies()
        for copy in copies:
            if (copy.active == True and copy.checked_out == 0):
                return (2, None)  # There is free copy
        Queue.red_button(doc)
        copies = doc.get_document_copies()  # update copies
        # if we have free copies after deleting queue, check out to users who are in request
        for copy in copies:
            if (copy.active == True and copy.checked_out == 0):
                res = self.check_out(doc, user)
                # One of copies became free after flushing the queue
                return (1, res)
        # Placing request
        res = Request.place_request(doc, user, self.librarian)
        return (0, res)  # Request is placed

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
            return (overdue_entries[(page - 1) * rows_number: page * rows_number], page_number)
        elif (opened == -1):
            select_query = History.select().where(History.date_return.is_null(False))
        else:
            return ([], 0)
        # Calculating number of pages
        page_number = int(select_query.count()) // rows_number
        if (select_query.count() % rows_number > 0):
            page_number += 1
        query = select_query.offset(
            0 + (page - 1) * rows_number).limit(rows_number)
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

        period = 7 * 2  # Some default period
        if (entry.renewed == False):
            period = user.group.get_checkout_time(doc) * 7
        else:
            period = user.group.get_renew_time(doc) * 7

        date_return = date_check_out + datetime.timedelta(days=period)
        return str(date_return)

    def check_overdue(self, entry):
        """Returns fine for overdue (0 if no fine)
        """
        period = 7 * 2  # Some default period
        doc = entry.copy.get_doc()
        if (entry.renewed == False):
            period = entry.user.group.get_checkout_time(doc) * 7
        else:
            period = entry.user.group.get_renew_time(doc) * 7
        date_return = entry.date_return
        if (date_return == None):  # if we are trying to check open entry
            date_return = str(datetime.date.today())
        res = min(self.overdue(entry.date_check_out, date_return,
                               period), entry.copy.get_doc().cost)
        return res

    def overdue(self, date_check_out, date_return, period):
        """Calculates fine
        """
        date_return_d = datetime.datetime.strptime(date_return, '%Y-%m-%d')
        date_check_out_d = datetime.datetime.strptime(
            date_check_out, '%Y-%m-%d')
        res = max((date_return_d - date_check_out_d).days -
                  period, 0) * self.__fine
        return res

    def pay_fine(self, usr, amount):
        """Pay fine of specific user.
        Returns change
        """
        usr.fine = max(usr.fine - amount, 0)
        return (max(amount - usr.fine, 0))
