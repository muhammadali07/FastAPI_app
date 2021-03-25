from mongoengine import *

class Users(Document):
    name = StringField(max_lenght=200, required=True)