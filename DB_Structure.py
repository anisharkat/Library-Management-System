from peewee import *
import datetime



db = MySQLDatabase('lb', user='root', password='anisharkat2005',
                         host='localhost', port=3306)


class Publisher(Model):
    name = CharField(unique = True)
    location = CharField(null = True)
    class Meta:
        database = db 

class Author(Model):
    name = CharField(unique = True)
    location = CharField(null = True)
    class Meta:
        database = db 

class Category(Model):
    category_name = CharField(unique = True)
    category_parent = IntegerField(null=True)
    class Meta:
        database = db  

class Branch(Model):
    name = CharField()
    code = CharField(null = True,unique = True)
    location = CharField(null = True)
    class Meta:
        database = db         


BOOKS_STATUS = (
    (1,'New'),
    (2,'Used'),
    (3,'Damaged')
)

class Books(Model):
    title = CharField(unique = True)
    description =TextField(null = True)
    category = ForeignKeyField(Category,backref='category',null = True)
    code = CharField(null = True)
    barcode = CharField()
    part_order =IntegerField(null = True)
    price = DecimalField(null = True)
    publisher = ForeignKeyField(Publisher,backref='publisher',null = True)
    author = ForeignKeyField(Author,backref='author',null = True) 
    image = CharField(null = True)
    status = CharField(choices=BOOKS_STATUS) 
    date = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db 


class Clients(Model):
    name = CharField()
    mail = CharField(null = True,unique = True)
    phone = CharField(null = True)
    date = DateField(default=datetime.datetime.now)
    national_id = IntegerField(null = True,unique = True)
    class Meta:
        database = db 

class Employee(Model):
    name = CharField()
    mail = CharField(null = True,unique = True)
    phone = CharField(null = True)
    date = DateField(default=datetime.datetime.now)
    national_id = IntegerField(null = True , unique = True)
    priority = IntegerField(null = True)
    class Meta:
        database = db 





PROCESS_TYPE = (
    (1,'Rent'),
    (2,'Retrive')
)

class Daily_movements(Model):
    book = ForeignKeyField(Books,backref='daily_book') 
    client = ForeignKeyField(Clients, backref='book_client')
    type = CharField(choices=PROCESS_TYPE) 
    date = DateTimeField(default=datetime.datetime.now)
    Branch = ForeignKeyField(Branch,backref='daily_branch',null = True)
    book_from = DateField(null = True) 
    book_to = DateField(null = True)
    employee = ForeignKeyField(Employee,backref='daily_employee',null = True)
    class Meta:
        database = db 


ACTION_TYPE = (
    (1,'Login'),
    (2,'Update'),
    (3,'Create'),
    (4,'Delete')
)


TABLE_CHOICES = (
    (1,'Books'),
    (2,'Clients'),
    (3,'Employee'),
    (4,'Category'),
    (5,'Branch'),
    (6,'Daily_movements'),
    (7,'Publisher'),
    (8,'Author'),
)

class History(Model):
    employee = ForeignKeyField(Employee,backref='history_employee')
    action = CharField(choices=ACTION_TYPE)
    table = CharField(choices=TABLE_CHOICES)
    date = DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch,backref='history_branch')
    class Meta:
        database = db 






db.connect()
db.create_tables([Author,Category,Branch,Publisher,Books,Clients,Employee,Daily_movements,History])
