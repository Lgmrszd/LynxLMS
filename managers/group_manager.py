from peewee import *
from db_connect import BaseModel


class Group(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    book_checkout_time = SmallIntegerField()
    book_bestseller_checkout_time = SmallIntegerField()
    journal_checkout_time = SmallIntegerField()
    av_checkout_time = SmallIntegerField()
    fields = {"id": id,
               "name": name,
               "book_checkout_time": book_checkout_time,
               "book_bestseller_checkout_time": book_bestseller_checkout_time,
               "journal_checkout_time": journal_checkout_time,
               "av_checkout_time": av_checkout_time}

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
        print(group)
        fields = cls.fields.copy()
        fields.pop("id")
        for key in fields.keys():
            if key in kwargs.keys():
                group.__dict__['_data'][key] = kwargs[key]
        group.save()

