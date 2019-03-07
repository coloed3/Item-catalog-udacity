# usr/bin/python3.71
from flask import Flask, request, render_template, redirect, flash, make_response,jsonify, url_for
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

#required_login decrorator

# from database_setup need to finish set up of db
from database_setup import Base, User, Category, Item, engine
# will call json file using global function for our file from google chrome
client_secrets = {}
# function below is used to open the file
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


    items = session.query(Item).order_by(Item.id.desc()).all()

    if request.path.endswith('.json'):
        return jsonify(json_list=[i.serialize for i in items])

    categories = session.query(Category).all()

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           section_title="Latest Items",
                           )


@app.route('/catalog/category/<int:category_id>/items')
@app.route('/catalog/category/<int:category_id>/items.json',
           endpoint="category-json")
def categoryItems(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(category_id=category.id).all()

    """Below will allow for user to view the .json endpoint"""
    if request.path.endswith('.json'):
        return jsonify(json_list=[i.serialize for i in items])




    return render_template(
        'catitems.html',
        category=category,
        items=items)


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



"""below taken from the course resturant application it does the following
allow user to be authicated by google, we save the token in session and use that 
to authorize user to make changes."""
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

    stored_credentials = login_session.get('access_token')

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
        user_id = create_user(login_session)
        login_session['user_id'] = user_id
    # will show welcome scren
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; '
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s!" % login_session['username'])
    print("Done!")
    return output


""" using information and code from restaurant project. to disconnect and close
sessions"""
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        login_session.clear()
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session.clear()
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        login_session.clear()
        return redirect(render_template('index.html'))

    return render_template('logout.html')

# logout current user and del sessions
@app.route('/logout')
def log_out():
    """will logout current user"""
    if 'username' in login_session:
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have been successfully logged out")
        return redirect(url_for('index'))
    else:
        flash('User was never logged in')
        return redirect(url_for('index'))


"""moving json to the bottom of the project, had to revamp to fit new database"""
"""route below allows user to add item_detail to viewitem.html"""
@app.route('/catalog/item/<int:item_id>/')
@app.route('/catalog/item/<int:item_id>/.json',
           endpoint="item-json")
def item_Details(item_id):

    item = session.query(Item).filter_by(id=item_id).first()
    category = session.query(Category) \
        .filter_by(id=item.category_id).first()
    if request.path.endswith('.json'):
        return jsonify(item.serialize)

    return render_template(
        'viewitem.html',
        category=category,
        item=item,
        )



#add items

"""Below will allow user to add item, after they login."""
@app.route('/item/add-item', methods=['GET', 'POST'])
def add_item():
    # "adding validation to adding new items"
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))


    elif request.method == 'POST':
        # Check if the item already exists in the database.
        # If it does, display an error.
        item = session.query(Item).filter_by(name=request.form['name']).first()
        if item:
            if item.name == request.form['name']:
                flash('The item already exists in the database!')
                return redirect(url_for("add_item"))
        new_item = Item(
            name=request.form['name'],
            category_id=request.form['category_name'],
            description=request.form['description'],
        )
        session.add(new_item)
        session.commit()
        flash('New item successfully created!')
        return redirect(url_for('index'))
    else:
        items = session.query(Item)
        categories = session.query(Category)
        return render_template(
            'additem.html',
            items=items,
            categories=categories
        )


""" below will allow the user to add a category to the
data base with authenicating if the category exist"""
@app.route('/catalog/add_category', methods=['GET', 'POST'])
def new_category():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    elif request.method == 'POST':
        if request.form['new-category-name'] == '':
            flash('The field cannot be empty.')
            return redirect(url_for('index'))

        category = session.query(Category).filter_by(name=request.form['new-category-name']).first()
        if category is not None:
            flash('The entered category already exists.')
            return redirect(url_for('new_category'))

        new_category = Category(
            name=request.form['new-category-name'])
        session.add(new_category)
        session.commit()
        flash('New category %s successfully created!' % new_category.name)
        return redirect(url_for('index'))
    else:
        return render_template('add_new_cat.html')



"""
Route below allows the user to select there desired category item (if they are logged in)
and will allow the name, description, cateogry type to be edited. 
"""
@app.route("/catalog/item/<int:item_id>/edit/", methods=['GET', 'POST'])
def edit_item(item_id):
    """Edit existing item."""
    item = session.query(Item).filter_by(id=item_id).first()

   


    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Item successfully updated!')
        return redirect(url_for('item_Details', item_id=item_id))
    else:
        categories = session.query(Category)
        return render_template(
            'edititem.html',
            item=item,
            categories=categories
        )


"""
Below route allows user if logged in to edit there category name. on the  edit_cat there
is authnication that the user will need to be logged in session to make changes. 
"""
@app.route('/catalog/category/<int:category_id>/edit/',
           methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit a category."""

    category = session.query(Category).filter_by(id=category_id).first()


    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
            session.add(category)
            session.commit()
            flash('Category successfully updated!')
            return redirect(url_for('categoryItems',category_id=category.id))
    else:
        return render_template('edit_cat.html', category=category)

    # if request.method == 'POST':
    #     if request.form['name']:
    #         item.name = request.form['name']
    #     if request.form['category_name']:
    #         item.category_name = request.form['category_name']
    #     if request.form['description']:
    #         item.description = request.form['description']
    #     if request.form['category']:
    #         category = session.query(Category).filter_by(name=request.form['category']).one()
    #         item.category = category
    #
    #     session.add(item)
    #     session.commit()
    #     flash('Category Item Successfully Edited!')
    #     return redirect(url_for('item_Details',
    #                             category_name=item.category.name))
    # else:
    #     categories=session.query(Category).all()
    #     return render_template('edititem.html',
    #                            item=item,
    #                            categories=categories)



# route for deletling

"""
Route below will be used for both the delete item and category
just switching the item_id to category_id. 
"""
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    """Authenication"""
    if 'username' not in login_session:
        flash('In order to delete any items please login')
        return redirect(url_for('showLogin'))
    item = session.query(Item).filter_by(id=item_id).first()

    if request.method=='POST':
        session.delete(item)
        session.commit()
        flash('Item was delete successfully')
        return redirect(url_for('index'))
    else:
        return render_template('deleteitem.html', item=item)

"""Route will delete category """
@app.route('/catalog/category/<int:category_id>/delete', methods=['GET', 'POST'])
def delete_category(category_id):
    """below will delete categories by id in the data base"""
    category = session.query(Category).filter_by(id=category_id).first()


    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash("Category successfully deleted!")
        return redirect(url_for('index'))
    else:
        return render_template("deletecat.html", category=category)


"""=========================================================================
code below taken from the restaurant application. 
==========================================================================="""


def create_user(login_session):
    """Crate a new user.

    Argument:
    login_session (dict): The login session.
    """

    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(new_user)
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



"""=======================================
  Json End points 
========================================="""

if __name__ == "__main__":
    """stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension,
    had issues with errors when attempting to login in to session"""
    app.secret_key = 'super_secret_key'
    load_json_secrets()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
