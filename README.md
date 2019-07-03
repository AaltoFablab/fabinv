# fabinv

The Fab Lab inventory. The easy way. 

Ever not been able to find stuff and to get started at a place like a Fab Lab? This tool is there to help you. It aims to be as simple as possible to help you manage and find stuff easily.

## Todo

- [x] For the backend Python would be the easiest I believe. Let's try the [graphene](https://github.com/graphql-python/graphene) GraphQL library and build a simple end-point which would return us a fake inventory table.
- [x] Backend: Add simple search to return items based on keyword provided.
- [x] Backend: Add real MongoDB database with instructions how to set up locally.
- [x] Backend: Add search across multiple fields and collections.
- [x] Backend: Add mutation to add new items and locations.
- [x] Backend: Add mutation to del items and locations.
- [x] Backend: Add mutation to mod items and locations.
- [ ] Backend: Add authentication mutations. [Password solution A](https://stackoverflow.com/questions/27943258/save-password-as-salted-hash-in-mongodb-in-users-collection-using-python-bcrypt), [Password solution B](https://pypi.org/project/passlib/).

- [x] Frontend: Create a fake search where on each input field change, GraphQL endpoint is called. Using [GraphQL.js](https://github.com/f/graphql.js) and [jQuery](https://jquery.com/).
- [x] Frontend: Integrate simple search feature from backend. 
- [ ] Frontent: Display item summary on click.
- [ ] Frontend: Add delete button for each item in the summary field.
- [ ] Frontend: Add edit and save for each item in the summary field.
- [ ] Frontend: Add login / logout functionality.
- [ ] Frontend: Port the solution to [RiotJS](https://riot.js.org/).

- [ ] CLI: `fabinv show locations` (returns locations with names and ids)
- [ ] CLI: `fabinv add item "Pepsi Max", 1.55, "location id"` (return item data)
- [ ] CLI: `fabinv add location "Fridge"` (return location name and id)

## Setting up MongoDB Instance

First, follow the instructions on the [official MongoDB documentation](https://docs.mongodb.com/manual/installation/) site to install MongoDB in the first place.

Start up your MongoDB instance. Make sure you know where your config file is.

```bash
mongo --port 27017 --config /usr/local/etc/mongod.conf
```

Connect to your MongoDB instance and add an admin user.

```bash
mongo --port 27017
```

```mongo
use admin
db.createUser(
  {
    user: 'fabadmin',
    pwd: 'thereisnofuture',
    roles: [ { role: 'root', db: 'admin' } ]
  }
)
```

Shut down MongoDB and exit `mongo` shell.

```mongo
db.adminCommand( { shutdown: 1 } )
exit
```

Start it again. This time with `--auth` flag.

```bash
mongod --auth --port 27017 --config /usr/local/etc/mongod.conf
```

Best would be if you would have mongodb running in the background as daemon. 

## Connecting to MongoDB and Creating Database

To create the `fabinv` database we need to use the `mongo` shell. Since we set up the username and password authentication in the previous step, use the following command to connect to the database via the `mongo` shell.

```bash
mongo --port 27017 -u "fabadmin" --authenticationDatabase "admin" -p
```

Enter password you provided in the DB setup step and you should see a `>` in front of your text cursor.

To create the `fabinv` database use the following.

```mongo
use fabinv
```

You won't be able to see it yet by using the `show dbs` command. It will become visible only after we insert at least one document. This will be done automatically during the **Setting up Python Environment** step.


## Setting up Python Environment

Start with making sure that you have Python 3 installed. 

```bash
python3 --version
# Python 3.7.3
```

**Optional**: To not mess up your existing Python ecosystem, make use of [Virtualenv](https://virtualenv.pypa.io/en/latest/). Install it with `pip3`. **Please use pip3!**

```bash
pip3 install virtualenv
```

**Optional**: Enter the project directory and set up virtualenv.

```bash
cd fabinv/backend
virtualenv env
source env/bin/activate
```

Install dependencies. If you set up vitualenv, `python` should be Python 3 and `pip` should map to `pip3`.

```bash
pip install -r requirements.txt
```

Run the backend application.

```bash
python app.py
# Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Open browser and open `http://127.0.0.1:5000/graphql`. Try out the following query.

```graphql
{ 
  items {
    name,
    location {
      name
    } 
  }
}
```

## Mutations

Mutations let you change the underlying database. Two basic ones are `addItem` and `addLocation` mutations. Location ID's are needed to add new items. Below you can see example GraphQL calls for both.

**Adding Locations**
```
mutation {
  addLocation(name: "3D Printing Room") {
    location {
      name
    }
  }
}
```

**Adding Items**
```
mutation {
  addItem(name: "Nails M2 30mm", price: 0.0, locationId: "5d1b0dcf036b2986fb8ccad7") {
    item {
      name,
      price,
      location {
        name
      }
    }
  }
}

```

## Development

1. Please read about [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) and [Semantic Versioning](https://semver.org/). 
2. Work in and commit changes to `develop` branch. 
3. If working something speciffic, create a feature branch.
