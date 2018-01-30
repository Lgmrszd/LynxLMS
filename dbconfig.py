from peewee import *

db = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


def init_db(host, password):
    db.init(
        "LynxLMS",
        user="admin",
        password=password,
        host=host
    )

