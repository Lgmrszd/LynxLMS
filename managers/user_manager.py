import peewee as pw
from managers.group_manager import Group
from db_connect import BaseModel


class User(BaseModel):
    """Data model for users and user's cards"""
    card_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    address = pw.CharField()
    phone = pw.BigIntegerField()
    fine = pw.SmallIntegerField(default=0)
    group = pw.ForeignKeyField(Group, related_name="users")
    fields = {"name": name,
              "surname": surname,
              "address": address,
              "phone": phone,
              "fine": fine,
              "group": group}

    @classmethod
    def get_by_id(cls, card_id):
        """Get user by id"""
        return cls.get(card_id=card_id)

    @classmethod
    def add(cls, kwargs):
        """Create a new user and add them to database"""
        return cls.create(**kwargs)

    @classmethod
    def remove(cls, card_id):
        """Remove excising user from database"""
        temp = cls.get(card_id=card_id)
        temp.delete_instance()

    @classmethod
    def edit(cls, card_id, **kwargs):
        """Edit certain values of user"""
        user = cls.get(card_id=card_id)
        fields = cls.fields.copy()
        fields.pop("id")
        for key in fields.keys():
            if key in kwargs.keys():
                user.__dict__['_data'][key] = kwargs[key]
        user.save()

    @classmethod
    def get_list(cls, rows_number, page):
        """Returns a content from certain page of user list"""
        query = cls.select().offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.name.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res

