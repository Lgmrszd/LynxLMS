import peewee as pw
from db_connect import BaseModel


class Document(BaseModel):
    DocumentID = pw.PrimaryKeyField()
    title = pw.CharField()
    author = pw.CharField()
    cost = pw.IntegerField()
    keywords = pw.CharField()
    #is_bestseller = pw.BooleanField(null = true, default=False)
    #is_reference = pw.BooleanField(null = true, default=False)

    @classmethod
    def add(cls, args):
        """Creates a new entity of selected type. Takes on input dictionary of values"""
        cls.create(**args)

    @classmethod
    def remove(cls, doc_id):
        """Removes an entity with specific DocumentID"""
        temp = cls.get(DocumentID=doc_id)
        print(temp.title)
        temp.delete_instance()
    
    @classmethod
    def edit(cls, doc_id, new_values):
        """Edit certain values in an entity with specific DocumentID"""
        temp = cls.get(DocumentID=doc_id)
        for k in new_values.keys():
            temp.__dict__['_data'][k] = new_values[k]
        temp.save()
        print(temp.__dict__)

    @classmethod
    def get_list(cls, rows_number, page):
        """Returns a content from ceratin page of document list"""
        query = cls.select().offset(0 + (page-1)*rows_number).limit(rows_number).order_by(cls.title.asc())
        res = []
        for entry in query:
            res.append(entry)
        return res

    @classmethod
    def get_fields(cls):
        """Returns list of fields of specific document type"""
        temp = {**cls.__dict__, **Document.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = []
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                res.append(key)
        return res
    
    @classmethod
    def get_fields_dict(cls):
        """Returns dictionary with field name as a key and type of field as a value"""
        map_to_types = {
            pw.IntegerField : int,
            pw.CharField : str,
            pw.TextField : str
        }
        temp = {**Document.__dict__, **cls.__dict__}
        temp.pop('__doc__')
        temp.pop('__module__')
        res = {}
        for key in temp.keys():
            if (isinstance(temp[key], pw.FieldDescriptor)):
                if (isinstance(temp[key].field, pw.IntegerField) | isinstance(temp[key].field, pw.BigIntegerField)):
                    res[key] = int
                elif (isinstance(temp[key].field, pw.CharField) | isinstance(temp[key].field, pw.TextField)):
                    res[key] = str
                elif (isinstance(temp[key].field, pw.BooleanField)):
                    res[key] = bool
                elif (isinstance(temp[key].field, pw.ForeignKeyField)):
                    res[key] = 'foreign'
        return res



class Book(Document):
    edition = pw.CharField()
    publisher = pw.CharField()
    year = pw.IntegerField()


class JournalArticle(Document):
    journal = pw.CharField()
    issue = pw.CharField()
    editor = pw.CharField()


class AVMaterial(Document):
    pass


class Copy(BaseModel):
    CopyID = pw.PrimaryKeyField()
    DocReference = pw.ForeignKeyField(Document, related_name = 'copies')
    checked_out = pw.BooleanField(default=False)
    storage = pw.CharField(default='')

    @classmethod
    def add(cls, args):
        cls.create(**args)
    
    @classmethod
    def edit_storage(cls, copy_id, new_storage):
        temp = cls.get(CopyID = copy_id)
        temp.storage = new_storage
        temp.save()


#clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
#for x in clsmembers:
#    if x[0] == 'BaseModel':
#        continue
#    Document._meta.database.create_table(x[1])