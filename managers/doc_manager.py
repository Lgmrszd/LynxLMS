import peewee as pw
from playhouse.postgres_ext import *
import json
from dbconfig import BaseModel


# remove next line in production
# db = pw.PostgresqlDatabase('test', user='user', password='test')

# class BaseModel (pw.Model):
#        class Meta:
#                database = db


class Document(BaseModel):
    DocumentID = pw.PrimaryKeyField()
    typeID = pw.IntegerField()
    name = pw.CharField()
    author = pw.CharField()
    isBestseller = pw.BooleanField()
    isReference = pw.BooleanField()
    details = JSONField()


class DocumentType(BaseModel):
    ID = pw.PrimaryKeyField()
    name = pw.CharField(unique=True)
    fields = pw.TextField()


def doc_manager_init():
    Document.create_table()
    DocumentType.create_table()


def add_document(name, doctype, author, isBestseller, isReference, details):
    try:
        # TODO: details json checker
        Document.create(type=doctype, name=name, author=author, isBestseller=isBestseller, isReference=isReference,
                        details=details)
    except ValueError:
        return 0
    return 1


def delete_document(DocumentID):
    try:
        # TODO: delete copies of this document
        doc = Document.get(DocumentID=DocumentID)
        doc.delete_instance()
    except pw.DatabaseError:
        return 0
    return 1


def add_type(name, fields=[], *args):
    name = str(name)

    for i in range(0, len(fields)):
        fields[i] = str(fields[i])

    DocumentType.create(name=name, fields=';'.join(fields))
    return 1
