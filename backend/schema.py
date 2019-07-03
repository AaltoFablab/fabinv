import graphene
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Location as LocationModel
from models import Item as ItemModel
from graphql import GraphQLError
from datetime import datetime

class Item(MongoengineObjectType):
    class Meta: 
        model = ItemModel
        description = 'The `Item` scalar holds data about an item in the fab inventory.'

class Location(MongoengineObjectType):
    class Meta:
        model = LocationModel
        description = 'The `Location` scalar describes a location of an `Item` in the fab inventory.'

class AddLocation(graphene.Mutation):
    '''
    Adds new location to database.
    `name` is required.
    '''

    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    location = graphene.Field(lambda: Location)

    def mutate(self, info, name):
        if name == '':
            raise GraphQLError('Location name must not be empty')
        
        # Check if location with the same name exists
        if LocationModel.objects(name__iexact=name).first() != None:
            raise GraphQLError('Location name must be unique')

        locationToStore = LocationModel(name=name)
        locationToStore.save()
        location = Location(name=name)
        ok = True
        return AddLocation(location=location, ok=ok)

class RemoveLocation(graphene.Mutation):
    '''
    Removes location with specified ID. 
    Throws error if items referencing location ID exist.
    Delete items or change their location before removing the location.
    '''

    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        if id == '':
            raise GraphQLError('Location ID must not be empty')

        # Check if we can find items with this location
        for item in ItemModel.objects:
            if str(item.location.id) == str(id):
                raise GraphQLError('Please delete items at the location first or change their location')
        
        # Try to delete
        if not LocationModel.objects(id=id).delete():
            raise GraphQLError('Location does not exist')
        
        ok = True
        return RemoveLocation(ok=ok)

class UpdateLocation(graphene.Mutation):
    '''
    Updates location in the database. Location `id` is required. 
    Everything else is optional and will not be changed if not specified.
    '''

    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: Location)

    def mutate(self, info, id, name=None):
        if id is '':
            raise GraphQLError('Location ID must not be empty')

        location = LocationModel.objects(id=id).first()
        if location is None:
            raise GraphQLError('Location not found')

        if name is not None:
            if name != location.name:
                location.name = name
                location.modified = datetime.now
                location.save()

        ok = True
        return UpdateLocation(ok=ok, location=location)

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
        if name == '':
            raise GraphQLError('Item name must not be empty')

        if locationId == '':
            raise GraphQLError('Location ID must not be empty')

        # Check if item with the same name exists
        if ItemModel.objects(name__iexact=name).first() != None:
            raise GraphQLError('Item name must be unique')

        locationFound = LocationModel.objects(id=locationId).first()
        if locationFound == None:
            raise GraphQLError('No location with ID found')

        # Location found, proceed with details
        itemToStore = ItemModel(name=name, price=price, location=locationFound)
        itemToStore.save()
        item = Item(name=name, price=price, location=locationFound)
        ok = True
        return AddItem(item=item, ok=ok)

class RemoveItem(graphene.Mutation):
    '''
    Removes an item with ID from database.
    '''

    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        if id == '':
            raise GraphQLError('Item ID must not be empty')
        
        # Try to delete
        if not ItemModel.objects(id=id).delete():
            raise GraphQLError('Item does not exist')

        ok = True
        return RemoveItem(ok=ok)

class UpdateItem(graphene.Mutation):
    '''
    Updates an item in the database. Item `id` is required. 
    Everything else is optional. Yes, you can specify `name`,
    `price` and `locationId` separately. What is not specified,
    will not be changed.
    '''

    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        price = graphene.Float()
        locationId = graphene.String()

    ok = graphene.Boolean()
    item = graphene.Field(lambda: Item)

    def mutate(self, info, id, name=None, price=None, locationId=None):
        item = ItemModel.objects(id=id).first()

        ok = True
        if item is None:
            raise GraphQLError('Item does not exist')

        if name is not None:
            if name != item.name:
                item.name = name
                item.modified = datetime.now

        if price is not None:
            if price != item.price:
                item.price = price
                item.modified = datetime.now

        if locationId is not None:
            location = LocationModel.objects(id=locationId).first()
            if location is None:
                raise GraphQLError('Could not find location')
            if location.id != item.location.id:
                item.location = location
                item.modified = datetime.now

        item.save()

        return UpdateItem(ok=ok, item=item)

class Mutations(graphene.ObjectType):
    add_item = AddItem.Field()
    remove_item = RemoveItem.Field()
    update_item = UpdateItem.Field()
    add_location = AddLocation.Field()
    remove_location = RemoveLocation.Field()
    update_location = UpdateLocation.Field()

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
