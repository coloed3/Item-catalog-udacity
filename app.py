# usr/bin/python3.71
from flask import Flask, request, render_template, redirect, flash, make_response, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
# from database_setup need to finish set up of db
from database_setup import Base, User, Category,Item, engine
# will call json file using global function for our file from google chrome
client_secrets ={}


app = Flask(__name__)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
engine = create_engine('sqlite:///catalogsdatabase.db')

"""Below will be the bases of the latest items"""
@app.route('/')
@app.route('/index')
@app.route('/index.json', endpoint="index-json")
def index():
    logged_in = is_logged_in()

    items = session.query(Item).order_by(Item.id.desc()).all()

    if request.path.endswith('.json'):
        return jsonify(json_list=[i.serialize for i in items])

    categories = session.query(Category).all()

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           logged_in=logged_in,
                           section_title="Latest Items",
                           )






@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>.json',
           endpoint="category-json")
def categoryItems(category_name):
    items = session.query(Item).filter_by(category_name=category_name).all()

    if request.path.endswith('.json'):
        return jsonify(json_list=[i.serialize for i in items])

    categories = session.query(Category).all()

    logged_in = is_logged_in()
    return render_template('index.html',
                           categories=categories,
                           current_category=category_name,
                           items=items,
                           logged_in=logged_in,
                           section_title="%s Items (%d items)" % (
                               category_name, len(items)),
                           )

# route for login
@app.route('/login')
def showLogin():
    return "This is a test"

# google+ oauth login route
@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    pass
    # will be using code used in the last project to brign over
    # will need to make sure the json files are working as intended


# gdisconnect    # with op
# @app.route('/gdisconne    # with opct')
# def gdisconnect():
#     pass
    # will use code from our last project  and will route to logout template


# route fdor seeing all our items

@app.route('/catalog/<string:category_name>/<string:item_name>')
def item_Details(category_name, item_name):
    return "this is cool"


# route for adding
@app.route('/catalog/addnew', methods=['GET', 'POST'])
def add_item():
   return render_template('additem.html')

# route for editing
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    return render_template('edititem.html')

# route for deletling
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    return render_template('deleteitem.html')



# ====== took this from our crud course for creating function for actions we need to preform
def is_logged_in():
    access_token = login_session.get('access_token')
    return access_token is not None
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
