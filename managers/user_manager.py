import peewee as pw
from managers.group_manager import Group
from db_connect import BaseModel


class User(BaseModel):
    card_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    address = pw.CharField()
    phone = pw.BigIntegerField()
    group = pw.ForeignKeyField(Group, related_name="users")
    _fields = {"card_id": "key",
                "name": "char",
                "surname": "char",
                "address": "char",
                "phone": "bigint",
                "group": "group"}

    @classmethod
    def add(cls, **kwargs):
        cls.create(**kwargs)

    @classmethod
    def remove(cls, card_id):
        temp = cls.get(card_id=card_id)
        temp.delete_instance()

    @classmethod
    def edit(cls, card_id, **kwargs):
        user = cls.get(card_id)
        for k in kwargs.keys():
            if k in cls._fields.keys():
                user.__dict__["_data"][k] = kwargs[k]
        user.save()

    @classmethod
    def get_fields(cls):
        return cls._fields