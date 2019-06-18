import graphene
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Location as LocationModel
from models import Item as ItemModel

class Item(MongoengineObjectType):
    class Meta: 
        model = ItemModel

class Location(MongoengineObjectType):
    class Meta:
        model = LocationModel

class Query(graphene.ObjectType):
    items = graphene.List(Item)
    locations = graphene.List(Location)
    
    def resolve_items(self, info):
        return list(ItemModel.objects.all())

    def resolve_locations(self, info):
        return list(LocationModel.objects.all())

schema = graphene.Schema(query=Query)
