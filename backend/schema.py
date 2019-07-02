import graphene
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Location as LocationModel
from models import Item as ItemModel
from graphql import GraphQLError

class Item(MongoengineObjectType):
    class Meta: 
        model = ItemModel
        description = 'The `Item` scalar holds data about an item in the fab inventory.'

class Location(MongoengineObjectType):
    class Meta:
        model = LocationModel
        description = 'The `Location` scalar describes a location of an `Item` in the fab inventory.'

class AddItem(graphene.Mutation):
    '''
    Adds new item to database. 
    `name`, `price` and `locationId` are requred.
    '''

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        locationId = graphene.String(required=True)

    ok = graphene.Boolean()
    item = graphene.Field(lambda: Item)

    def mutate(self, info, name, price, locationId):
        locationFound = LocationModel.objects(id=locationId).first()
        if locationFound == None:
            raise GraphQLError('No location with ID found')

        # Location found, proceed with details
        itemToStore = ItemModel(name=name, price=price, location=locationFound)
        itemToStore.save()
        item = Item(name=name, price=price, location=locationFound)
        ok = True
        return AddItem(item=item, ok=ok)

class Mutations(graphene.ObjectType):
    add_item = AddItem.Field()

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

            # Start by looking for first terms first
            for term in terms:
                for item in all_items:
                    if term.lower() in item.name.lower():
                        found_items.append(item)
                        continue
                    if term.lower() in item.location.name.lower():
                        found_items.append(item)
                        continue
                    if term.lower() in str(item.price):
                        found_items.append(item)
                        continue

            # Make sure we do not include duplicates and maintain order
            # https://stackoverflow.com/a/7961390/1753004
            return list(dict.fromkeys(found_items))
        else:
            return all_items;

    def resolve_locations(self, info):
        return list(LocationModel.objects.all().order_by('name'))

schema = graphene.Schema(query=Query, mutation=Mutations)
