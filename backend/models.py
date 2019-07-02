from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField, FloatField, BooleanField,
)

class Created(Document):
    meta = {'collection': 'created'}
    yes = BooleanField(default=True)
    modified = DateTimeField(default=datetime.now)

class Location(Document):
    meta = {'collection': 'locations'}
    name = StringField(required=True)
    modified = DateTimeField(default=datetime.now)

class Item(Document):
    meta = {'collection': 'items'}
    name = StringField(required=True)
    location = ReferenceField(Location)
    price = FloatField(required=True)
    modified = DateTimeField(default=datetime.now)
