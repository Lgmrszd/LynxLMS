from lynxlms_server import BaseModel
import peewee as pw


class DocType(BaseModel):
    name = pw.CharField()
    fields = pw.CharField()


class Document(BaseModel):
    document_id = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()
    doc_type = pw.ForeignKeyField(DocType, related_name="documents")


class Group(BaseModel):
    groups_id = pw.PrimaryKeyField()
    name = pw.TextField()
    rules = pw.CharField()


tables = [DocType, Document, Group]
