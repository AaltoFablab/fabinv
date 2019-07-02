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
    locations_description = 'Returns an array of locations in the fab inventory. All locations are returned, ordered by name.'
    locations = graphene.List(Location, description = locations_description)

    # http://docs.mongoengine.org/guide/querying.html
    def resolve_items(self, info, search):
        all_items = ItemModel.objects.all()
        found_items = []

        if search != '':
            terms = search.split()
            for item in all_items:
                if any(term.lower() in item.name.lower() for term in terms):
                    found_items.append(item)
                    continue
                if any(term.lower() in item.location.name.lower() for term in terms):
                    found_items.append(item)
                    continue
                if any(term.lower() in str(item.price) for term in terms):
                    found_items.append(item)
                    continue

            def sort_by_name(elem):
                return elem.name

            found_items.sort(key=sort_by_name)
            return found_items
        else:
            return all_items;

    def resolve_locations(self, info):
        return list(LocationModel.objects.all().order_by('name'))

schema = graphene.Schema(query=Query)
