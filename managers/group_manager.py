from peewee import *
from db_connect import BaseModel
from managers.doc_manager import class_to_name


class Group(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    book_ct = SmallIntegerField()
    book_bestseller_ct = SmallIntegerField()
    journal_ct = SmallIntegerField()
    av_ct = SmallIntegerField()
    fields = {"id": id,
              "name": name,
              "book_ct": book_ct,
              "book_bt": book_bestseller_ct,
              "journal_ct": journal_ct,
              "av_ct": av_ct}

    @classmethod
    def get_by_id(cls, g_id):
        return cls.get(id=g_id)

    @classmethod
    def add(cls, **kwargs):
        cls.create(**kwargs)

    @classmethod
    def remove(cls, g_id):
        temp = cls.get(id=g_id)
        temp.delete_instance()

    @classmethod
    def edit(cls, g_id, **kwargs):
        group = cls.get(id=g_id)
        fields = cls.fields.copy()
        fields.pop("id")
        for key in fields.keys():
            if key in kwargs.keys():
                group.__dict__['_data'][key] = kwargs[key]
        group.save()

    def get_checkout_time(self, doc):
        doc_type = class_to_name()[type(doc)]
        if doc_type == "Book":
            return self.book_ct
        elif doc_type == "JournalArticle":
            return self.journal_ct
        elif doc_type == "AVMaterial":
            return self.av_ct

    @classmethod
    def get_list(cls, rows_number, page):
        """Returns a content from certain page of group list"""
        query = cls.select().offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.name.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res
