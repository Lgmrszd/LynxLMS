import peewee as pw
import json
import sys
import inspect
from dbconfig import BaseModel

class Document(BaseModel):
    DocumentID = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()

    @classmethod
    def add(cls, args):
        """Creates a new entity of selected type. Takes on input dictionary of values"""
        cls.create(**args)

    @classmethod
    def remove(cls, doc_id):
        """Removes an entity with specific DocumentID"""
        temp = cls.get(DocumentID = doc_id)
        print(temp.title)
        temp.delete_instance()
    
    @classmethod
    def edit(cls, doc_id, new_values):
        """Edit certain values in an entity with specific DocumentID"""
        temp = cls.get(DocumentID = doc_id)
        for k in new_values.keys():
            temp.__dict__['_data'][k] = new_values[k]
        temp.save()
        print(temp.__dict__)

    @classmethod
    def get_list(cls, page):
        """Returns a content from ceratin page of document list"""
        query = cls.select().offset(0 + (page-1)*15).limit(15).order_by(cls.title.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def get_fields(cls):
        """Returns list of fields of specific document type"""
        temp = {**cls.__dict__ , **Document.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = []
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                res.append(key)
        return res

class Book(Document):
    edition = pw.CharField()
    publisher = pw.CharField()
    year = pw.IntegerField()

class Journal_article(Document):
    journal = pw.CharField()
    issue = pw.CharField()
    editor = pw.CharField()

class AV_material(Document):
    pass

#clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
#for x in clsmembers:
#    if x[0] == 'BaseModel':
#        continue
#    Document._meta.database.create_table(x[1])