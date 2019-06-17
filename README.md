# fabinv

The Fab Lab inventory. The easy way. 

Ever not been able to find stuff and to get started at a place like a Fab Lab? This tool is there to help you. It aims to be as simple as possible to help you manage and find stuff easily.

## Next Steps

One could try the README-driven-development strategy here.

- [ ] For the backend Python would be the easiest I believe. Let's try the [graphene](https://github.com/graphql-python/graphene) GraphQL library and build a simple end-point which would return us a fake inventory table.
- [ ] For that GraphQL endpoint, let's build a front-end. Which framework to use has to be decided, but we could go with RiotJS and JQuery, using Skeleton for style initially.

## Setting up

In order to not mess up your existing Python ecosystem, make use of [Virtualenv](https://virtualenv.pypa.io/en/latest/). Install it with `pip`. **Please use Python3!**

```
pip3 install virtualenv
```

Enter the project directory and set it up. Some parts of this have been taken from the [Graphene Mongo](https://graphene-mongo.readthedocs.io/en/latest/tutorial.html#setup-the-project) project.

```
virtualenv env
source env/bin/activate

# Install required packages
pip install Flask
pip install Flask-GraphQL
pip install graphene-mongo

# Install mongomock or you have to run a real mongo server instance somewhere.
pip install mongomock
```

