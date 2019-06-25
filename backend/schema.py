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
    items = graphene.List(Item, search=graphene.String(required=False))
    locations = graphene.List(Location)
    
    # http://docs.mongoengine.org/guide/querying.html
    def resolve_items(self, info, search=''):
        if(search != ''):
            options = {
                'name__icontains' : search
            }
            return list(ItemModel.objects(**options))[:10]
        return list(ItemModel.objects.all().order_by('name'))[:10]

    def resolve_locations(self, info):
        return list(LocationModel.objects.all().order_by('name'))

schema = graphene.Schema(query=Query)
