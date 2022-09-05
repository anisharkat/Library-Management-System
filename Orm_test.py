from peewee import *

# Connect to a MySQL database on network.
db = MySQLDatabase('library', user='root', password='anisharkat2005',
                         host='localhost', port=3306)


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database


  
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Pet])