import peewee as pw
from db_connect import BaseModel
import sys
import inspect


class Document(BaseModel):
    """Base data model for all document classes
    """
    DocumentID = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()
    active = pw.BooleanField(default=True)

    def get_document_copies(self):
        """Get list of copies of speciific document
        """
        doc_class = class_to_name()[type(self)]
        query = Copy.select().where(Copy.docClass == doc_class , Copy.docId == self.DocumentID)
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def get_by_id(cls, doc_id):
        """Get document by id
        """
        return cls.get(DocumentID = doc_id)
    
    @classmethod
    def add(cls, args):
        """Creates a new entity of selected type. Takes on input dictionary of values
        """
        return cls.create(**args)

    @classmethod
    def remove(cls, doc_id):
        """Removes an entity with specific DocumentID
        """
        entry = cls.get(DocumentID = doc_id)
        entry.active = False
        entry.save()
        copies = cls.get_document_copies(entry)
        for c in copies:
            Copy.remove(c.CopyID)
        
    
    @classmethod
    def edit(cls, doc_id, new_values):
        """Edit certain values in an entity with specific DocumentID
        """
        temp = cls.get(DocumentID=doc_id)
        for k in new_values.keys():
            temp.__dict__['_data'][k] = new_values[k]
        temp.save()
        print(temp.__dict__)

    #TODO : Add number of pages
    #Use SQL count() for pages

    @classmethod
    def get_list(cls, rows_number, page, active=0):
        """Returns a content from certain page of document list
        """
        #Active - 1, Not active = -1, All = 0
        if (active == 0):
            query = cls.select().offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.title.asc())
        elif (active == 1):
            query = cls.select().where(cls.active == True).offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.title.asc())
        elif (active == -1):
            query = cls.select().where(cls.active == False).offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.title.asc())
        else:
            return([])
        res = []
        for entry in query:
            res.append(entry)
        return res
    
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
    def get_fields_dict(cls):
        """Returns dictionary with field name as a key and type of field as a value
        """
        map_to_types = {
            pw.IntegerField : int,
            pw.CharField : str,
            pw.TextField : str
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



class Book(Document):
    """Data model for Book
    """
    edition = pw.CharField()
    publisher = pw.CharField()
    year = pw.IntegerField()


class JournalArticle(Document):
    """Data model for Journal Article
    """
    journal = pw.CharField()
    issue = pw.CharField()
    editor = pw.CharField()


class AVMaterial(Document):
    """Data model for Audio Video Material
    """
    pass


class Copy(BaseModel):
    """Data model for Copy
    """
    CopyID = pw.PrimaryKeyField()
    #DocReference = pw.ForeignKeyField(Document, related_name = 'copies')
    docClass = pw.CharField()
    docId = pw.IntegerField()
    active = pw.BooleanField(default=True)
    checked_out = pw.BooleanField(default=False)
    storage = pw.CharField(default='')

    #TODO : Add get_by_id

    def get_doc(self):
        """Get the document to which this copy referred
        """
        doc_class = name_to_class()[self.docClass]
        return doc_class.get_by_id(self.docId)
    
    @classmethod
    def add(cls, doc):
        """Add copy of specific document
        """
        #Activate document if it is deactivated
        return cls.create(docClass = class_to_name()[type(doc)], docId = doc.DocumentID)
    
    @classmethod
    def edit_storage(cls, copy_id, new_storage):
        """Edit storage place for specific copy
        """
        temp = cls.get(CopyID = copy_id)
        temp.storage = new_storage
        temp.save()
    
    @classmethod
    def remove(cls, copy_id):
        """Removes (deactivates) copy"""
        entry = cls.get(CopyID = copy_id)
        entry.active = False
        entry.save()
        #Check number of active copies of document. If zero - deactivate document
        #if (len(entry.get_doc.get_list(10,1,1)) == 0):
        #   doc = entry.get_doc
        #    doc.active = False
        #    doc.save()


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