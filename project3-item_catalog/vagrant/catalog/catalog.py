"""
Main python file that performs url routing and get/post responses.
"""

import datetime
import hashlib
import httplib2
import json
import requests
from catalog_db_setup import Base, Cuisines, Dishes, Users
from catalog_helpers import *
from flask import Flask, render_template, url_for, request,\
                  redirect, flash, jsonify, abort, make_response
from flask import Session as login_session
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from os import path, mkdir
from os import remove as os_remove
from sqlalchemy import create_engine, desc
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from urllib import unquote
from werkzeug import secure_filename

app = Flask(__name__)

engine = create_engine('sqlite:///cuisines.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

BASE_GOOGLEAPI_URI = "https://www.googleapis.com/oauth2/v1/"


def login_required(f):
    """
    Decorator function with login check and redirect.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in flask_session:
            return redirect(url_for('userLogin', next=request.url))
        else:
            return f(*args, **kwargs)
    return decorated_function


def createUser(user_data):
    """
    This function deals with the insertion of new users into the db.
    Returns the user_id of the object.
    """
    # Get user e-mail and name from input data to create a new user.
    newUser = Users(email=user_data['email'],
                    name=user_data['name'])

    # Insert new user into the database.
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(
        email=user_data['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    Returns the user associated with the user_id.
    """
    try:
        user = session.query(Users).filter_by(
            id=user_id).one()
        return user
    except NoResultFound:
        return None


def getUserId(e_mail):
    """
    Returns the user_id associated with the given e-mail address.
    """
    try:
        user = session.query(Users).filter_by(
            email=e_mail).one()
        return user.id
    except NoResultFound:
        return None


@app.errorhandler(404)
def page_not_found(err):
    """
    Route for a custom http 404 error page.
    """
    return render_template('404.html'), 404


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    This function deals handling a Google OAuth2 response.
    Based on Source From Full Stack Foundations course:
      https://github.com/udacity/ud330/blob/master/Lesson2/step5/project.py
    """
    # Ensure that the state anti-forgery variable matches.
    if request.args.get('state') != flask_session['state']:
        response = make_response(
                    json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Upgrade the authorization code into a credentials object.
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade ' +
                                 'the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the returned access token is valid using Google's API.
    access_token = credentials.access_token
    url = BASE_GOOGLEAPI_URI+('tokeninfo?access_token=%s' % access_token)
    result = json.loads(httplib2.Http().request(url, 'GET')[1])

    # If there is an error of some sort, return an error response code.
    if result.get('error') is not None:
        response = make_response(json.dumps('error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("GConnect: OAuth response received:", result)

    # Check the given gplus_id matches the current user id.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID does not " +
                                            "match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already logged in.
    if flask_session.get('credentials') is not None and \
       flask_session.get('gplus_id') == gplus_id:
        response = make_response(json.dumps("Current user is already " +
                                            "connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the user details into the session.
    flask_session['credentials'] = credentials
    flask_session['gplus_id'] = gplus_id

    # Retreive user info from credentials object.
    userinfo_url = BASE_GOOGLEAPI_URI+"userinfo"
    params = {'access_token': credentials.access_token,
              'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # Retreive and store the resulting user data.
    data = answer.json()
    flask_session['username'] = data['name']
    flask_session['picture'] = data['picture']
    flask_session['email'] = data['email']

    # Check if this user is already in our local database.
    user = session.query(Users).filter_by(email=data['email'])
    try:
        user = user.one()
    except NoResultFound, e:
        # If not, then add the user to the database
        createUser(data)

    # Generate an output div and image for the login confirmation.
    output = "<h1>Welcome "
    output += flask_session['username']
    output += '!</h1><img class="img-responsive img-rounded" src="'
    output += flask_session['picture']
    output += '">'
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    This function will terminate a users google oauth session.
    Source:
        https://github.com/udacity/ud330/blob/master/Lesson2/step6/project.py
    """
    credentials = flask_session.get('credentials')

    # Generate a different response if the user is not logged in
    if credentials is None:
        response = make_response(json.dumps("Current user is not" +
                                            " connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Send HTTP Get request to Google API to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/' +\
          ('revoke?token=%s' % credentials.access_token)
    result = httplib2.Http().request(url, 'GET')[0]

    # If successful, reset all of the user's credentials.
    if result['status'] == '200':
        del flask_session['credentials']
        del flask_session['gplus_id']
        del flask_session['username']
        del flask_session['email']
        del flask_session['picture']

        response = make_response(json.dumps("User successfully" +
                                            "disconnected."), 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps("Failed to revoke user" +
                                            "access token."), 400)
        response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/login')
def userLogin():
    """
    Renders template for login and calls the login function.
    """
    # Check if the user is already logged in.
    if 'username' in flask_session:
        return redirect(url_for('index'))
    state = generateRandomString()
    flask_session['state'] = state
    next = None
    next = request.args.get('next')
    if next:
        next = unquote(next)
    else:
        next = url_for('index')
    return render_template('login.html', STATE=state, NEXT=next)


@app.route("/logout")
def userLogout():
    """
    Calls disconnect function and redirects user to primary landing page.
    """
    gdisconnect()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    """
    Render a default landing page.
    """
    # Check if user is logged in for template rendering.
    if 'username' not in flask_session:
        username = None
    else:
        username = flask_session['username']

    # Query for 3 most recently inserted dishes.
    cuisineList = session.query(Cuisines).all()
    recentDishes = session.query(Dishes).order_by(
                    desc(Dishes.creation_time)).limit(3).all()

    # Calculate different in time from creation time to now.
    timeDeltas = []
    for dish in recentDishes:
        time = datetime.datetime.now().replace(microsecond=0)
        creation_time = dish.creation_time.replace(microsecond=0)
        time_diff = time-creation_time
        timeDeltas.append(time_diff)

    return render_template('index.html',
                           cuisines=cuisineList,
                           dishes=recentDishes,
                           times=timeDeltas,
                           path_check=path.isfile,
                           user=username)


@app.route('/cuisines/new/', methods=['GET', 'POST'])
@login_required
def newCuisine():
    """
    Handles inserting a new cuisine type into the database.
    """
    username = flask_session['username']
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        _name = request.form['name']
        _name = correctCasing(_name)
        cuisine = session.query(Cuisines).filter_by(name=_name)
        try:
            cuisine = cuisine.one()
            flash(u'\"%s\" not added. Cuisine already exists.' % _name)
            return render_template("cuisineform.html",
                                   cu_id=cuisine.id,
                                   user=username)
        except NoResultFound, e:
            pass
        # Create a new Cuisine tuple and add it to the Database.
        newCuis = Cuisines(name=_name,
                          owner_id=getUserId(flask_session['email']))
        session.add(newCuis)
        session.commit()
        return redirect(url_for('index'))
    else:
        # If a GET request, just render a blank form
        return render_template("cuisineform.html",
                               user=username)


@app.route('/cuisines/<int:c_id>/view')
def viewCuisine(c_id):
    """
    Finds the associated cuisine_id and then rends a page
    with all of the dishes associated with it.
    """
    # Check if user is logged in for template rendering.
    if 'username' not in flask_session:
        username = None
    else:
        username = flask_session['username']

    # Search for the cuisine-id.
    cuisine = session.query(Cuisines).filter_by(id=c_id)
    try:
        cuisine = cuisine.one()
    except NoResultFound, e:
        abort(404)
    # Get all the dishes associated with the id.
    dishes = session.query(Dishes).filter_by(cuisine_id=c_id)
    try:
        dishes = dishes.all()
    except NoResultFound, e:
        dishes = None
    return render_template('cuisineview.html',
                           dishes=dishes,
                           cuisine=cuisine,
                           user=username)


@app.route('/cuisine/<int:c_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCuisine(c_id):
    """
    Deletes a cuisine associated with the cuisine-id.
    """
    username = flask_session['username']

    # Search for the cuisine-id.
    _cuisine = session.query(Cuisines).filter_by(id=c_id)
    try:
        _cuisine = _cuisine.one()
    except NoResultFound, e:
        abort(404)

    # Ensure the user trying to delete this item is the owner.
    if int(getUserId(flask_session['email'])) != int(_cuisine.owner_id):
        abort(401)

    # If get request, respond with a confirmation page.
    if request.method == 'GET':
        return render_template('cuisinedelete.html',
                               cuisine=_cuisine,
                               user=username)

    # If a post request, delete the item from the db.
    elif request.method == 'POST':
        session.delete(_cuisine)
        session.commit()
        flash(u'\"%s\" deleted.' % _cuisine.name)
        return redirect(url_for('index'))


@app.route('/cuisines/<int:c_id>/new', methods=['GET', 'POST'])
@login_required
def newDish(c_id):
    """
    Add a new dish to the database, associated with a cuisine-id.
    """
    username = flask_session['username']

    # Search the database for the cuisine-id.
    _cuisine = session.query(Cuisines).filter_by(id=c_id)
    try:
        _cuisine = _cuisine.one()
    except NoResultFound, e:
        # No entry matching the cuisine-id found, render an error page.
        abort(404)
    # If found, check the HTTP request type.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        _name = request.form['name']
        _name = correctCasing(_name)
        _desc = request.form['description']
        _dish = session.query(Dishes).filter_by(name=_name)
        img = request.files['image']
        img_path = "static/img/default.jpg"

        try:
            _dish = _dish.one()
            # Dish already exists in database, do not add to db.
            flash(u'%s has previously been submitted.' % _name)
            return render_template('dishform.html',
                                   cuisine_id=c_id,
                                   dish_id=_dish.id,
                                   user=username)
        except NoResultFound, e:
            pass

        # Insert a new dish into the database.
        now = datetime.datetime.now().replace(microsecond=0)
        newDish = Dishes(name=_name,
                         description=_desc,
                         cuisine=_cuisine,
                         cuisine_id=_cuisine.id,
                         image_path=img_path,
                         creation_time=now,
                         owner_id=getUserId(flask_session['email']))
        session.add(newDish)
        session.flush()

        # Create the directories for image storage and save the image file.
        if img:
            img_path = ["static/img", str(newDish.cuisine_id), str(newDish.id)]
            _path = img_path[0]
            for subpath in img_path[1:]:
                _path += "/"
                _path += subpath
                if not path.exists(path.abspath(_path)):
                    mkdir(path.abspath(_path))
            img_path = _path + "/" + secure_filename(img.filename)
            img.save(img_path)
            newDish.image_path = img_path

        session.commit()

        flash(u'%s dish successfully added.' % _name)
        return render_template('dishform.html',
                               cuisine_id=c_id,
                               dish_id=newDish.id)
    elif request.method == 'GET':
        # If a GET request, just render a form.
        return render_template('dishform.html',
                               cuisine_id=c_id)


@app.route('/cuisines/<int:c_id>/dishes/<int:d_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editDish(c_id, d_id):
    """
    Edit the details of a dish in the database.
    """
    username = flask_session['username']

    # Search the database for the given dish.
    _dish = session.query(Dishes).filter_by(id=d_id)
    try:
        _dish = _dish.one()
    # If no entry matching the dish-id found, render an error page.
    except NoResultFound, e:
        abort(404)

    # Also check that the cuisine-id is correct.
    if _dish.cuisine.id != c_id:
        abort(404)

    # Ensure the user trying to edit this item is the owner.
    if int(getUserId(flask_session['email'])) != int(_dish.cuisine.owner_id):
        abort(401)

    # If found, check the HTTP request type.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        _name = request.form['name']
        _desc = request.form['description']
        img = request.files['image']

        # Check the name was changed
        if _name == "":
            _name = _dish.name

        # Make sure a dish with this name doesn't already exist.
        else:
            _name = correctCasing(_name)
            try:
                temp = _dish
                _dish = session.query(Dishes).filter_by(name=_name).one()
                # Dish already exists in database, do not add to db.
                flash(u'%s already exists. Edit failed.' % _name)
                return render_template('dishedit.html',
                                       cuisine_id=c_id,
                                       dish=temp,
                                       user=username)
            except NoResultFound, e:
                pass
        # Update the dish's details in the database.
        _dish.name = _name
        if _desc != "":
            _dish.description = _desc
        if img:
            img_path = ["static/img", str(_dish.cuisine_id), str(_dish.id)]
            _path = img_path[0]
            for subpath in img_path[1:]:
                _path += "/"
                _path += subpath
                if not path.exists(path.abspath(_path)):
                    mkdir(path.abspath(_path))
            img_path = _path + "/" + secure_filename(img.filename)
            # Delete old image file, if it exists.
            if path.isfile(img_path):
                print("deleting old file")
                os_remove(img_path)
            # Save new image file.
            print("saving new file")
            img.save(img_path)
            _dish.image_path = img_path

        _dish.edit_time = datetime.datetime.now()

        session.commit()

        # Notify the front-end that the update was successful.
        flash(u'%s successfully updated.' % _name)
        return render_template('dishedit.html',
                               cuisine_id=c_id,
                               dish=_dish,
                               user=username)

    # If a GET request, just render a blank form.
    else:
        return render_template('dishedit.html',
                               cuisine_id=c_id,
                               dish=_dish,
                               user=username)


@app.route('/cuisines/<int:c_id>/dishes/<int:d_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteDish(c_id, d_id):
    """
    This function will deal with deleting a dish from the database.
    """
    username = flask_session['username']

    # First check the dish exists.
    _dish = session.query(Dishes).filter_by(id=d_id)
    try:
        _dish = _dish.one()
    # No entry matching the dish-id found, render an error page.
    except NoResultFound, e:
        abort(404)

    # Check that the cuisine-id is correct.
    if _dish.cuisine_id != c_id:
        abort(404)

    # Ensure the user trying to delete this item is the owner.
    if int(getUserId(flask_session['email'])) != int(_dish.cuisine.owner_id):
        abort(401)

    # Get request results in a confirmation check.
    if request.method == 'GET':
        return render_template('dishdelete.html',
                               cuisine_id=_dish.cuisine_id,
                               dish=_dish,
                               user=username)

    # Post request results in deleting the dish from the db.
    elif request.method == 'POST':
        os_remove(_dish.image_path) 
        session.delete(_dish)
        session.commit()
        flash(u'\"%s\" deleted.' % _dish.name)
        return redirect(url_for('index'))


@app.route('/cuisines/<int:c_id>/dishes/<int:d_id>/view')
def viewDish(c_id, d_id):
    """
    This function will deal with listing a dish's details.
    """
    if 'username' not in flask_session:
        username = None
    else:
        username = flask_session['username']

    # Search the database for the given dish.
    _dish = session.query(Dishes).filter_by(id=d_id)

    try:
        _dish = _dish.one()
    # If no entry matching the dish-id found, render an error page.
    except NoResultFound, e:
        abort(404)

    # Also check that the cuisine-id is correct.
    if _dish.cuisine.id != c_id:
        abort(404)

    return render_template("dishview.html",
                           cuisine_id=c_id,
                           dish=_dish,
                           user=username,
                           path_check=path.isfile)


@app.route('/cuisines/<int:c_id>/dishes/<int:d_id>/JSON')
def viewDishJSON(c_id, d_id):
    _dish = session.query(Dishes).filter_by(id=d_id)
    try:
        _dish = _dish.one()
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        abort(404)

    # Also check that the cuisine-id is correct.
    if _dish.cuisine.id != c_id:
        return jsonify(None)

    return jsonify(dish=[_dish.serialize])


if __name__ == "__main__":
    app.debug = True
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SECRET_KEY"] = "a_Secret_Key"
    flask_session = login_session()
    app.run(host='0.0.0.0', port=5000)
