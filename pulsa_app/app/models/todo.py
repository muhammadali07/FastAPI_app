from mongoengine import *
from app.models.user import Users

class Todos(Document):
    title = StringField(max_lenght=200, required=True)
    description = StringField()
    owner = LazyReferenceField(Users, reverse_delete_rule = CASCADE) #LazyReferenceField sama dengan foreig key, reverse_delete_rule konsepnya seperti on delete cascade di mysql