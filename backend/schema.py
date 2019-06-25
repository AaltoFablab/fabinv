import graphene
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Location as LocationModel
from models import Item as ItemModel

class Item(MongoengineObjectType):
    class Meta: 
        model = ItemModel
        description = 'The `Item` scalar holds data about an item in the fab inventory.'

class Location(MongoengineObjectType):
    class Meta:
        model = LocationModel
        description = 'The `Location` scalar describes a location of an `Item` in the fab inventory.'

class Query(graphene.ObjectType):
    items_description = 'Returns an array of items in the fab inventory. Use the `search` argument to filter them. If no arguments are provided, all items are returned, ordered by name.'
    items = graphene.List(Item, search = graphene.String( required = False, default_value = '' ), description = items_description)
    locations_description = 'Returns an array of locations in the fab inventory. All locations are returnes, ordered by name.'
    locations = graphene.List(Location, description = locations_description)
    
    # http://docs.mongoengine.org/guide/querying.html
    def resolve_items(self, info, search):
        if(search != ''):
            options = {
                'name__icontains' : search
            }
            return list(ItemModel.objects(**options))[:10]
        return list(ItemModel.objects.all().order_by('name'))

    def resolve_locations(self, info):
        return list(LocationModel.objects.all().order_by('name'))

schema = graphene.Schema(query=Query)
