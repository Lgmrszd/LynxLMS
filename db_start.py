import peewee as pw
import dbconfig
import managers.doc_manager
import managers.user_manager
import managers.group_manager

#Connecting database
dbconfig.db.connect()

#mgrs.dbconfig.db.connect()

#Creating tables
dbconfig.db.create_tables([managers.doc_manager.Book,
    managers.doc_manager.AV_material,
    managers.doc_manager.Journal_article,
    managers.user_manager.User,
    managers.group_manager.Group ], safe = True)

