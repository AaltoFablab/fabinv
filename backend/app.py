from database import init_db
from flask import Flask, render_template
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__, template_folder='../frontend')
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run()
