import datetime
import logging

import peewee as pw

import managers.doc_manager as doc_manager
import managers.notifier
from db_connect import BaseModel
from managers import event_manager, task_manager
from managers.auth import require_auth_class
from managers.group_manager import Group


@require_auth_class()
class User(BaseModel):
    """Data model for users and user's cards"""
    card_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    address = pw.CharField()
    phone = pw.BigIntegerField()
    email = pw.CharField()
    fine = pw.SmallIntegerField(default=0)
    group = pw.ForeignKeyField(Group, related_name="users")
    fields = {"name": name,
              "surname": surname,
              "address": address,
              "phone": phone,
              "email": email,
              "fine": fine,
              "group": group}

    @classmethod
    def get_by_id(cls, card_id):
        """Get user by id"""
        user = cls.get(card_id=card_id)
        return user

    @classmethod
    def add(cls, kwargs):
        """Create a new user and add them to database"""
        if len(cls.get_list_all(1, 1)) == 0:
            kwargs["card_id"] = 1000
        return cls.create(**kwargs)

    @classmethod
    def remove(cls, card_id):
        """Remove excising user from database"""
        # Delete entries in queues
        current_user = cls.get_by_id(card_id)
        Queue.delete().where(Queue.user == current_user, Queue.active is True).execute()
        select_query = Queue.select().where(Queue.user == current_user)
        for entry in select_query:
            copy = entry.assigned_copy
            copy.checked_out = 0
            copy.save()
            # Maybe inform user at this point
        Queue.delete().where(Queue.user == current_user).execute()
        # Cancel outstanding request
        select_query = Request.select().where(Request.user == current_user, Request.active is True)
        for entry in select_query:
            # Check if it is only active entry in requests with such document and cancel request
            if (len(Request.select().where(Request.docClass == entry.docClass,
                                           Request.docId == entry.docId,
                                           Request.active is True)) == 1):
                # getting document from request entry
                doc = doc_manager.name_to_class()[entry.docClass].get_by_id(entry.docId)
                doc.cancel_request()
        Request.update(active=False).where(Request.user == current_user,
                                           Request.active is True).execute()  # Possible bug here!
        # Deleting user (moving to group deleted)
        deleted = Group.get_deleted()
        cls.edit(card_id, {"group": deleted})

    @classmethod
    def edit(cls, card_id, kwargs):
        """Edit certain values of user"""
        user = cls.get(card_id=card_id)
        fields = cls.fields.copy()
        for key in fields.keys():
            if key in kwargs.keys():
                user.__dict__['_data'][key] = kwargs[key]
        user.save()

    @classmethod
    def get_list(cls, rows_number, page, search=None):
        """Returns a content from certain page of user list"""
        query = cls.select().where(cls.group != 1)
        if search:
            query = cls.search(query, search)
        query = query.order_by(cls.name.asc()).offset(0 + (page - 1) * rows_number).limit(rows_number)
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def get_list_all(cls, rows_number, page):
        """Returns a content from certain page of user list"""
        query = cls.select().offset(0 + (page - 1) * rows_number).limit(rows_number).order_by(cls.name.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def search(cls, query, search):
        """According to fields and values in search dictionary,
           use additional conditions on the query
        """
        fields = cls._get_fields_dict_raw()
        for key in search.keys():
            if key in fields.keys():
                if isinstance(fields[key], pw.IntegerField) or isinstance(fields[key], pw.BigIntegerField):
                    query = query.where(fields[key] == int(search[key][0]))
                elif isinstance(fields[key], pw.CharField) or isinstance(fields[key], pw.TextField):
                    if search[key][1]:
                        query = query.where(fields[key] == search[key][0])
                    else:
                        search_string = '%' + str(search[key][0]) + '%'
                        query = query.where(fields[key] ** search_string)
                elif isinstance(fields[key], pw.BooleanField):
                    query = query.where(fields[key] == bool(search[key][0]))
                elif fields[key] == managers.group_manager.Group:
                    query = query.where(User.group == search[key][0])
        return query

    @classmethod
    def _get_fields_dict_raw(cls):
        """Returns dictionary with field name as a key and peewee type of the field as a value
        """
        temp = {**User.__dict__, **cls.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = {}
        for key in temp.keys():
            if isinstance(temp[key], pw.FieldDescriptor):
                res[key] = temp[key].field
        res["group"] = managers.group_manager.Group
        return res


def remove_from_group(group_id):
    users = User.select().where(User.group == group_id)
    for user in users:
        User.remove(user.card_id)


event_manager.register_listener("remove_users_from_group", remove_from_group)


class Queue(BaseModel):
    """Data model for document queue
    """
    QueueID = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(User, related_name='queue')
    priority = pw.SmallIntegerField()
    docClass = pw.CharField()
    docId = pw.IntegerField()
    assigned_copy = pw.ForeignKeyField(doc_manager.Copy, related_name='reserved', null=True)
    time_out = pw.DateField(formats='%Y-%m-%d', null=True)
    active = pw.BooleanField(default=True)  # if user is in

    def get_doc(self):
        """Get the document to which this copy referred
        """
        doc_class = doc_manager.name_to_class()[self.docClass]
        return doc_class.get_by_id(self.docId)

    @classmethod
    def push_to_queue(cls, doc, user):
        """Pushes user to queue for specific document
        """
        # Check if user is already in queue
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        select_query = Queue.select().where(Queue.user == user, Queue.active is True,
                                            Queue.docClass == doc_class,
                                            Queue.docId == doc_id)
        if len(select_query) == 1:
            return None
        elif len(select_query) > 1:
            # print('Houston, we have a problem in booking system in push_to_queue')
            logging.error('Queue.push_to_queue, 2 or more same active entries (2 same users in the queue)')
            return None

        return Queue.create(docClass=doc_class, docId=doc_id, user=user, priority=user.group.priority)

    @classmethod
    def get_to_remove(cls, doc, user):
        """Get entry from queue that should be deleted after check out
        """
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        # Get all entries from queue containing this user and document
        ent = Queue.select().where(Queue.user == user,
                                   Queue.docClass == doc_class, Queue.docId == doc_id,
                                   Queue.active is False)
        if len(ent) == 0:
            return None  # Nothing to check out
        if len(ent) > 1:
            # Problem in the database or with peewee
            # print('Houston, we have a problem in queue in get_to_remove')
            logging.error('Queue.get_to_remove(), 2 same entries in the queue!')
            return None
        return ent.get()

    @classmethod
    def get_queue_entry(cls, doc):
        """Gets entry from queue.
        """
        # Find earliest with higher prority
        select_query = Queue.select(Queue.priority).where(Queue.docClass == doc_manager.class_to_name()[type(doc)],
                                                          Queue.docId == doc.DocumentID,
                                                          Queue.active is True).distinct()
        # if queue is empty
        if len(select_query) == 0:
            return None
        # Find max priority
        max_priority = -1
        for entry in select_query:
            if entry.priority > max_priority:  # possible bug due to no entries
                max_priority = entry.priority

        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID

        entry = Queue.select().where(Queue.docClass == doc_class, Queue.docId == doc_id,
                                     Queue.priority == max_priority,
                                     Queue.active is True).get()  # check if return least id
        # TODO : Try to optimize
        return entry

    @classmethod
    def get_user_from_queue(cls, copy):
        """Get highest priority user from queue for document of specific copy and assign this copy to user
        """
        doc = copy.get_doc()
        res = cls.get_queue_entry(doc)
        if res is None:
            return None
        time_out_date = datetime.date.today() + datetime.timedelta(days=1)
        res.time_out = str(time_out_date)
        res.assigned_copy = copy
        res.active = False
        res.save()
        copy.checked_out = 1
        copy.save()
        return res.user

    @classmethod
    def update_queue(cls):
        """Update queue. Delete all overdue entries
        """
        select_query = Queue.select().where(Queue.active is False)
        current_date = datetime.date.today()
        users = []
        for entry in select_query:
            time_out_date = datetime.datetime.strptime(entry.time_out, '%Y-%m-%d').date()
            if current_date >= time_out_date:
                # inform user here
                doc_class = doc_manager.name_to_class()[entry.docClass]
                doc = doc_class.get_by_id(entry.docId)
                managers.notifier.notify_request_overdue([entry.user], doc)
                users.append(entry.user)
                copy = entry.assigned_copy
                if cls.get_user_from_queue(copy) is None:
                    copy.checked_out = 0
                    copy.save()
                entry.delete_instance()
        return users

    @classmethod
    def red_button(cls, doc):
        """Outstanding request to delete queue for specific document
        """
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        select_query = Queue.select().where(Queue.docClass == doc_class, Queue.docId == doc_id)
        users = []
        # TODO : Replace code below with 2-3 queries!!!
        for entry in select_query:
            users.append(entry.user)  # inform user
            # text = "Dear %s,\nQueue for the document \"%s\" have been abandoned due to outstanding request.\n"\
            #        % (entry.user.name + " " + entry.user.surname, doc.title)
            # managers.notifier.send_message(entry.user.email, "Document queue abandoned", text)
            entry.delete_instance()
        managers.notifier.notify_doc_abandon(users, doc)
        copies = doc.get_document_copies()
        res = []
        for copy in copies:
            if copy.checked_out == 1:
                copy.checked_out = 0
                copy.save()
                res.append(copy)
        return res

    @classmethod
    def get_list(cls, doc, rows_number, page, active=0):  # TODO : rework arguments
        """Returns a content from certain page of waiting list (queue)
        Active - active=1, Not active - active=-1, All - active=0
        """
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        if active == 0:
            select_query = cls.select().where(cls.docClass == doc_class, cls.docId == doc_id)
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number).order_by(Queue.priority.asc(),
                                                                                                  Queue.QueueID.desc(),
                                                                                                  Queue.active.asc())
        elif active == 1:
            select_query = cls.select().where(cls.active is True, cls.docClass == doc_class, cls.docId == doc_id)
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number).order_by(Queue.priority.asc(),
                                                                                                  Queue.QueueID.desc())
        elif active == -1:
            select_query = cls.select().where(cls.active is False, cls.docClass == doc_class, cls.docId == doc_id)
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number).order_by(Queue.priority.asc(),
                                                                                                  Queue.QueueID.desc())
        else:
            return [], 0
        res = []
        for entry in query:
            res.append(entry)
        # Counting number of pages
        page_number = int(select_query.count()) // rows_number
        if select_query.count() % rows_number > 0:
            page_number += 1
        return res, page_number


def __update_queue_task_func(_1, _2):
    Queue.update_queue()
    new_date = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    task_manager.Task.create(
        datetime=new_date,
        func_name="update_queue",
        display_name="Update queue",
        parameters=[True]
    )
    return task_manager.FINISHED, "Queue updated"


task_manager.register_task_function("update_queue", __update_queue_task_func)


class Request(BaseModel):
    request_id = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(User, related_name='requests')
    docClass = pw.CharField()
    docId = pw.IntegerField()
    date = pw.DateField(formats='%Y-%m-%d')
    librarian = pw.CharField()
    active = pw.BooleanField(default=True)

    @classmethod
    def place_request(cls, doc, user, librarian):
        """Place outstanding request for certain user for certain document (conditions should be checked)"""
        doc.enable_request()
        current_date = datetime.date.today()
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        res = cls.create(user=user, docClass=doc_class, docId=doc_id, date=str(current_date), librarian=librarian)
        # Queue.red_button(doc)
        return res

    @classmethod
    def close_request(cls, user, doc):
        """Close outstanding request for certain user and document"""
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        entry = Request.select().where(Request.user == user, Request.docClass == doc_class,
                                       Request.docId == doc_id, Request.active is True)
        if entry.count() > 1:
            # print("Houston, check close_request in Request")
            logging.error('Request.close_request(), 2 same active entries in the Request table')
            return 1
        if entry.count() == 0:
            return 1
        entry = entry.get()
        entry.active = False
        entry.save()
        if (len(Request.select().where(Request.docClass == doc_class, Request.docId == doc_id,
                                       Request.active is True)) == 0):
            doc.cancel_request()
        return 0

    @classmethod
    def get_user(cls, doc):
        """Get user from outstanding request for certain document"""
        doc_class = doc_manager.class_to_name()[type(doc)]
        doc_id = doc.DocumentID
        entry = Request.select().where(Request.docClass == doc_class, Request.docId == doc_id,
                                       Request.active is True)
        if len(entry) == 0:
            return None
        return entry.get().user

    @classmethod
    def get_list(cls, rows_number, page, active=0):  # TODO : rework arguments
        """Returns a content from certain page of requests list
        Active - active=1, Not active - active=-1, All - active=0
        """
        if active == 0:
            select_query = cls.select()
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number)
        elif active == 1:
            select_query = cls.select().where(cls.active is True)
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number)
        elif active == -1:
            select_query = cls.select().where(cls.active is False)
            query = select_query.offset(0 + (page - 1) * rows_number).limit(rows_number)
        else:
            return [], 0
        res = []
        for entry in query:
            res.append(entry)
        # Counting number of pages
        page_number = int(select_query.count()) // rows_number
        if select_query.count() % rows_number > 0:
            page_number += 1
        return res, page_number
