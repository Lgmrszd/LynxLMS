import peewee as pw
import json
from dbconfig import BaseModel


class Document(BaseModel):
    DocumentID = pw.PrimaryKeyField()
    typeID = pw.IntegerField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()

    @classmethod
    def get_fields(cls):
        temp = {**cls.__dict__ , **Document.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        return temp.keys()

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

