import peewee as pw
from db_connect import BaseModel
import sys
import inspect
from managers.auth import require_auth_class
import managers.event_manager as event_manager


class Document(BaseModel):
    """Base data model for all document classes
    """
    DocumentID = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()
    active = pw.BooleanField(default=True)
    requested = pw.BooleanField(default=False)

    def get_document_copies(self):
        """Get list of copies of speciific document
        """
        doc_class = class_to_name()[type(self)]
        query = Copy.select().where(Copy.docClass == doc_class,
                                    Copy.docId == self.DocumentID)
        res = []
        for entry in query:
            res.append(entry)
        return res

    def enable_request(self):
        self.requested = True
        self.save()

    def cancel_request(self):
        self.requested = False
        self.save()

    @classmethod
    def get_by_id(cls, doc_id):
        """Get document by id
        """
        return cls.get(DocumentID=doc_id)

    @classmethod
    def add(cls, args):
        """Creates a new entity of selected type. Takes on input dictionary of values
        """
        return cls.create(**args)

    @classmethod
    def remove(cls, doc_id):
        """Removes an entity with specific DocumentID
        """
        entry = cls.get(DocumentID=doc_id)
        entry.active = False
        entry.save()
        # Removing all copies
        doc_class = class_to_name()[cls]
        update_query = Copy.update(active=False).where(Copy.docClass == doc_class,
                                                       Copy.docId == doc_id, Copy.active == True)
        update_query.execute()

    @classmethod
    def edit(cls, doc_id, new_values):
        """Edit certain values in an entity with specific DocumentID
        """
        temp = cls.get(DocumentID=doc_id)
        for k in new_values.keys():
            temp.__dict__['_data'][k] = new_values[k]
        temp.save()

    @classmethod
    def get_list(cls, rows_number, page, active=0, search={}):  # TODO : rework arguments
        """Returns a content from certain page of document list
        Active - active=1, Not active - active=-1, All - active=0
        Search query structure :
        {'Field name': ('Your query', 'strict')}, where strict, means
        strict search for strings for True and otherwise for False.
        For other types it could be either True or False
        """
        select_query = None
        if (active == 0):
            select_query = cls.select()
            select_query = cls.search(select_query, search)
            query = select_query.order_by(cls.title.asc()).offset(
                0 + (page-1)*rows_number).limit(rows_number)
        elif (active == 1):
            select_query = cls.select().where(cls.active == True)
            select_query = cls.search(select_query, search)
            query = select_query.order_by(cls.title.asc()).offset(
                0 + (page-1)*rows_number).limit(rows_number)
        elif (active == -1):
            select_query = cls.select().where(cls.active == False)
            select_query = cls.search(select_query, search)
            query = select_query.order_by(cls.title.asc()).offset(
                0 + (page-1)*rows_number).limit(rows_number)
        else:
            return([], 0)
        res = []
        for entry in query:
            res.append(entry)
        # Counting number of pages
        page_number = int(select_query.count()) // rows_number
        if (select_query.count() % rows_number > 0):
            page_number += 1
        return res, page_number
    
    @classmethod
    def search(cls, query, search):
        """Accorfing to fields and values in search dictionary,
           use additional conditions on the query
        """
        fields = cls._get_fields_dict_raw()
        for key in search.keys():
            search_query = search[key][0]
            strict = search[key][1]
            if key in fields.keys():
                field = fields[key]
                if (isinstance(field, pw.IntegerField) or isinstance(field, pw.BigIntegerField)):
                    query = query.where(field == int(search_query))
                elif (isinstance(field, pw.CharField) or isinstance(field, pw.TextField)):
                    if key is 'keywords':   #TODO : Find better solution if possible
                        for keyword in search_query:
                            search_string = '%' + str(keyword).strip() + '%'
                            query = query.where(field ** search_string)
                    else:
                        if strict:
                            query = query.where(field == str(search_query).strip())
                        else:
                            search_string = '%' + str(search_query).strip() + '%'
                            query = query.where(fields[key] ** str(search_string).strip())
                elif (isinstance(field, pw.BooleanField)):
                    query = query.where(field == bool(search_query))
        return query

    @classmethod
    def get_fields(cls):
        """Returns list of fields of specific document type
        """
        temp = {**Document.__dict__, **cls.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = []
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                res.append(key)
        return res

    @classmethod
    def _get_fields_dict_raw(cls):
        """Returns dictionary with field name as a key and peewee type of the field as a value
        """
        temp = {**Document.__dict__, **cls.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = {}
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                res[key] = temp[key].field
        return res

    @classmethod
    def get_fields_dict(cls):
        """Returns dictionary with field name as a key and type of the field as a value
        """
        map_to_types = {
            pw.IntegerField: int,
            pw.CharField: str,
            pw.TextField: str
        }
        temp = {**Document.__dict__, **cls.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = {}
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                if (isinstance(temp[key].field, pw.IntegerField) or isinstance(temp[key].field, pw.BigIntegerField)):
                    res[key] = int
                elif (isinstance(temp[key].field, pw.CharField) or isinstance(temp[key].field, pw.TextField)):
                    res[key] = str
                elif (isinstance(temp[key].field, pw.BooleanField)):
                    res[key] = bool
                elif (isinstance(temp[key].field, pw.ForeignKeyField)):
                    res[key] = 'foreign'
        return res


@require_auth_class()
class Book(Document):
    """Data model for Book
    """
    edition = pw.CharField()
    publisher = pw.CharField()
    year = pw.IntegerField()


@require_auth_class()
class JournalArticle(Document):
    """Data model for Journal Article
    """
    journal = pw.CharField()
    issue = pw.CharField()
    editor = pw.CharField()


@require_auth_class()
class AVMaterial(Document):
    """Data model for Audio Video Material
    """
    pass


@require_auth_class()
class Copy(BaseModel):
    """Data model for Copy
    """
    CopyID = pw.PrimaryKeyField()
    #DocReference = pw.ForeignKeyField(Document, related_name = 'copies')
    docClass = pw.CharField()
    docId = pw.IntegerField()
    active = pw.BooleanField(default=True)
    #checked_out = pw.BooleanField(default=False)
    # 0 - not cheked out, 1 - reserved, 2 - checked out
    checked_out = pw.SmallIntegerField(default=0)
    storage = pw.CharField(default='')

    def get_doc(self):
        """Get the document to which this copy referred
        """
        doc_class = name_to_class()[self.docClass]
        return doc_class.get_by_id(self.docId)

    @classmethod
    def get_by_id(cls, copy_id):
        return cls.get(CopyID=copy_id)

    @classmethod
    def add(cls, doc, storage=''):
        """Add copy of specific document
        """
        res = cls.create(docClass=class_to_name()[
                         type(doc)], docId=doc.DocumentID)
        # Activate document if it is deactivated
        if (doc.active == False):
            doc.active = True
            doc.save()
        event_manager.send_event('free_copy', res)
        return res

    @classmethod
    def edit_storage(cls, copy_id, new_storage):
        """Edit storage place for specific copy
        """
        temp = cls.get(CopyID=copy_id)
        temp.storage = new_storage
        temp.save()

    @classmethod
    def remove(cls, copy_id):
        """Removes (deactivates) copy"""
        entry = cls.get(CopyID=copy_id)
        entry.active = False
        entry.save()
        # Check number of active copies of document. If zero - deactivate document
        doc = entry.get_doc()
        doc_class = class_to_name()[type(doc)]
        query = Copy.select().where(Copy.docClass == doc_class,
                                    Copy.docId == doc.DocumentID,
                                    Copy.active == True).count()
        if (query == 0):
            doc.active = False
            doc.save()

    @classmethod
    def restore(cls, copy_id):
        """Restores deleted copy"""
        entry = cls.get_by_id(copy_id)
        entry.active = True
        entry.save()
        doc = entry.get_doc()
        if (doc.active == False):
            doc.active = True
            doc.save()


def name_to_class():
    """Returns a map that has names of classes as keys and classes as values
    """
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    res = {}
    for c in classes:
        res[c[0]] = c[1]
    return res


def class_to_name():
    """Returns a map that has classes as keys and class names as values
    """
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    res = {}
    for c in classes:
        res[c[1]] = c[0]
    return res
