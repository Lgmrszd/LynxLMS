from peewee import *
from playhouse.migrate import *
from db_connect import BaseModel
from managers.doc_manager import class_to_name


class Group(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    book_ct = SmallIntegerField()
    book_bestseller_ct = SmallIntegerField()
    journal_ct = SmallIntegerField()
    av_ct = SmallIntegerField()
    book_rt = SmallIntegerField()
    book_bestseller_rt = SmallIntegerField()
    journal_rt = SmallIntegerField()
    av_rt = SmallIntegerField()
    priority = SmallIntegerField()
    fields = {"name": name,
              "book_ct": book_ct,
              "book_bestseller_ct": book_bestseller_ct,
              "journal_ct": journal_ct,
              "av_ct": av_ct,
              "book_rt": book_ct,
              "book_bestseller_rt": book_bestseller_ct,
              "journal_rt": journal_ct,
              "av_rt": av_ct,
              "priority": priority}

    @classmethod
    def get_by_id(cls, g_id):
        return cls.get(id=g_id)

    @classmethod
    def add(cls, kwargs):
        return cls.create(**kwargs)

    @classmethod
    def remove(cls, g_id):
        temp = cls.get(id=g_id)
        temp.delete_instance()

    @classmethod
    def edit(cls, g_id, kwargs):
        group = cls.get(id=g_id)
        fields = cls.fields.copy()
        for key in fields.keys():
            if key in kwargs.keys():
                group.__dict__['_data'][key] = kwargs[key]
        group.save()

    def get_checkout_time(self, doc):
        doc_type = class_to_name()[type(doc)]
        if doc_type == "Book" and not ('best seller' in doc.keywords):
            return self.book_ct
        elif doc_type == "Book" and 'best seller' in doc.keywords:
            return self.book_bestseller_ct
        elif doc_type == "JournalArticle":
            return self.journal_ct
        elif doc_type == "AVMaterial":
            return self.av_ct
    
    def get_renew_time(self, doc):
        doc_type = class_to_name()[type(doc)]
        if doc_type == "Book" and not ('best seller' in doc.keywords):
            return self.book_rt
        elif doc_type == "Book" and 'best seller' in doc.keywords:
            return self.book_bestseller_rt
        elif doc_type == "JournalArticle":
            return self.journal_rt
        elif doc_type == "AVMaterial":
            return self.av_rt

    @classmethod
    def get_list(cls, rows_number, page):
        """Returns a content from certain page of group list"""
        query = cls.select().offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.name.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def get_deleted(cls):
        deleted = Group.get(Group.name == "Deleted")
        return deleted
