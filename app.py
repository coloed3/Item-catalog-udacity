# usr/bin/python3.71
from flask import Flask, request, render_template, redirect, flash, make_response, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
import random
import string
import httplib2
import os
import json
import requests
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
# from database_setup need to finish set up of db
from database_setup import Base, User, Category,Item, engine

# will call json file using global function for our file from google chrome
client_secrets={}
#function below is used to open the file
"""======================================================================="""
def load_json_secrets():
    global client_secrets
    client_secrets = json.load(open('client_secrets.json'))['web']

"""=========================================================================="""

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
# below code taken from restaurant app and modified for this project.
# get_token() is a function that will allow for us to "encrypt" the string
@app.route('/login')
def showLogin():
    access_token = login_session.get('access_token')

    if access_token is None:
        state = getToken()
        login_session['state'] = state

        return render_template('login.html', STATE=state,
                               CLIENT_ID=client_secrets['client_id'])
    else:
        return render_template('loginin.html')

# google+ oauth login route
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:

        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID didn't match the given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != client_secrets['client_id']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = AccessTokenCredentials(
        login_session.get('access_token'), 'user-agent-value')

    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("completed")
    return output

    # will be using code used in the last project to brign over
    # will need to make sure the json files are working as intended





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

"""=========================================================================
code below taken from the restaurant application. 
==========================================================================="""
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# ====== took this from our crud course for creating function for actions we need to preform
def is_logged_in():
    access_token = login_session.get('access_token')
    return access_token is not None

# ===== Function used for login in encryption
def getToken():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))


if __name__ == "__main__":
    """stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension,
    had issues with errors when attempting to login in to session"""
    app.secret_key = 'super_secret_key'
    load_json_secrets()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
