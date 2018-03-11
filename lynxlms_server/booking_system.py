import peewee as pw
import datetime
from lynxlms_server import BaseModel, User, Copy
from uuid import uuid4 as uuid


class Librarian(BaseModel):
    librarian_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    password = pw.CharField()


class Entry(BaseModel):
    operations_id = pw.PrimaryKeyField()
    user = pw.ForeignKeyField(User, related_name='operations')
    copy = pw.ForeignKeyField(Copy, related_name='operations')
    librarian_checked_out = pw.ForeignKeyField(Librarian, related_name='checked_out_entries')
    librarian_returned = pw.ForeignKeyField(Librarian, related_name='returned_entries')
    date_check_out = pw.DateField(formats='%Y-%m-%d')
    date_deadline = pw.DateField(formats='%Y-%m-%d', null=True)
    date_return = pw.DateField(formats='%Y-%m-%d', null=True)


class Session(BaseModel):
    uuid = pw.CharField(default=uuid(), primary_key=True)
    librarian = pw.ForeignKeyField(Librarian, backref="librarian")
    logged_date = pw.DateTimeField(default=datetime.datetime.now)
    active = pw.BooleanField(default=True)

    def logout(self):
        self.active = False


booking_system_tables = [Librarian, Entry, Session]
