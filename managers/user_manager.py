import peewee as pw
from managers.group_manager import Group
from db_connect import BaseModel


class User(BaseModel):
    card_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    address = pw.CharField()
    phone = pw.BigIntegerField()
    fine = pw.SmallIntegerField()
    group = pw.ForeignKeyField(Group, related_name="users")
    fields = {"name": name,
              "surname": surname,
              "address": address,
              "phone": phone,
              "fine": fine,
              "group": group}

    @classmethod
    def get_by_id(cls, card_id):
        return cls.get(card_id=card_id)

    @classmethod
    def add(cls, **kwargs):
        cls.create(**kwargs)

    @classmethod
    def remove(cls, card_id):
        temp = cls.get(card_id=card_id)
        temp.delete_instance()

    @classmethod
    def edit(cls, card_id, **kwargs):
        user = cls.get(card_id=card_id)
        fields = cls.fields.copy()
        fields.pop("id")
        for key in fields.keys():
            if key in kwargs.keys():
                user.__dict__['_data'][key] = kwargs[key]
        user.save()

