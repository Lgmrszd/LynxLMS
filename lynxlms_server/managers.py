from lynxlms_server import BaseModel
import peewee as pw
import json


class DocType(BaseModel):
    doc_type_id = pw.PrimaryKeyField()
    name = pw.CharField()
    fields = pw.CharField()

    def get_additional_fields_names(self):
        return [k for k in json.loads(str(self.fields)).keys()]

    def get_additional_fields_types(self):
        return json.loads(str(self.fields))


class Document(BaseModel):
    document_id = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()
    additional_fields = pw.CharField()
    doc_type = pw.ForeignKeyField(DocType, related_name="documents")

    main_fields_names = ["title", "author", "cost", "keywords"]

    def get_main_fields(self):
        return {
            "title": str(self.title),
            "author": str(self.author),
            "cost": int(str(self.cost)),
            "keywords": str(self.keywords)
        }

    def get_additional_fields(self):
        return json.loads(str(self.additional_fields))

    def get_main_fields_names(self):
        return self.main_fields_names

    def get_additional_fields_names(self):
        return [k for k in json.loads(str(self.additional_fields)).keys()]

    def get_fields(self):
        fields = self.get_main_fields()
        fields.update(self.get_additional_fields())
        return fields

    @classmethod
    def create(cls, **query):
        doc_type = query["doc_type"]
        if type(doc_type) == str:
            doc_type = DocType.get(DocType.name == doc_type)

        fields = {k: query[k] for k in query if k in cls.main_fields_names}

        additional_fields = {k: query[k] for k in query if k not in cls.main_fields_names and k is not "doc_type"}
        additional_fields_types = doc_type.get_additional_fields_types()
        for k in additional_fields.keys():
            if type(additional_fields[k]).__name__ != additional_fields_types[k]:
                raise TypeError

        fields["doc_type"] = doc_type
        fields["additional_fields"] = json.dumps(additional_fields)
        return super().create(**fields)


class Group(BaseModel):
    group_id = pw.PrimaryKeyField()
    name = pw.TextField()
    rules = pw.CharField()


class User(BaseModel):
    user_id = pw.PrimaryKeyField()
    name = pw.CharField()
    surname = pw.CharField()
    address = pw.CharField()
    phone = pw.BigIntegerField()
    fine = pw.SmallIntegerField(default=0)
    group = pw.ForeignKeyField(Group, related_name="users")
    active = pw.BooleanField(default=True)

    def get_fields(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "address": self.address,
            "fine": self.fine,
            "group": self.group.group_id,
            "active": self.active
        }


class Copy(BaseModel):
    copy_id = pw.PrimaryKeyField()
    document_id = pw.ForeignKeyField(Document, related_name='copies')
    active = pw.BooleanField(default=True)
    checked_out = pw.BooleanField(default=False)
    storage = pw.CharField(default='')


managers_tables = [DocType, Document, Group, User, Copy]
