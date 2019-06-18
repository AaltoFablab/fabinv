from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField, FloatField,
)

class Location(Document):
    meta = {'collection': 'location'}
    name = StringField(required=True)
    modified = DateTimeField(default=datetime.now)

class Item(Document):
    meta = {'collection': 'item'}
    name = StringField(required=True)
    location = ReferenceField(Location)
    price = FloatField(required=True)
    modified = DateTimeField(default=datetime.now)
