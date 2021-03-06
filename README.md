# fabinv

The Fab Lab inventory. The easy way. 

Ever not been able to find stuff and to get started at a place like a Fab Lab? This tool is there to help you. It aims to be as simple as possible to help you manage and find stuff easily.

## Next Steps

One could try the README-driven-development strategy here.

- [x] For the backend Python would be the easiest I believe. Let's try the [graphene](https://github.com/graphql-python/graphene) GraphQL library and build a simple end-point which would return us a fake inventory table.
- [ ] Backend: Add simple search to return items based on keyword provided.
- [ ] For that GraphQL endpoint, let's build a front-end. Which framework to use has to be decided, but we could go with RiotJS and JQuery, using Skeleton for style initially.

## Setting up

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

```jquery
{ 
  items {
    name,
    location {
      name
    } 
  }
}
```

## Development

1. Please read about [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) and [Semantic Versioning](https://semver.org/). 
2. Work in and commit changes to `develop` branch. 
3. If working something speciffic, create a feature branch.
