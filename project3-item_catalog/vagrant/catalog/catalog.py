"""
Main python file that performs url routing and get/post responses.
"""

from flask import Flask, render_template, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Cuisine, Dishes, Users

engine = create_engine('sqlite:///cookbook.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from os import urandom

import hashlib

@app.route('/login/')
def userLogin(username, password):
    """
    This function deals with user login.
    """
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        email = request.form['E-mail']
        password = request.form['password']
        # Search the db for the user based on e-mail address.
        user = session.query(User).filter_by(email=email)
        # Check if there was a result.
        try: 
            user = user.one()
        except NoResultFound, e:
            #username not found
            return #render_template('login.html', bad_account=True)
        # Compare hash of password+salt to stored hash value.
        hashed = hashlib.sha256(password+cuisine.salt)
        if cuisine.sha256_password == hashed:
            #password matches
            #login(username)
            return #redirect(url_for('myAccount', user=username)
        else:
            #password does not match
            return #render_template('login.html', bad_account=True)
    elif request.method == 'GET':
        # If a GET request, just render a login form.
        return render_template('login.html', bad_account=False)
    return render_template('error.html')

@app.route('/createuser/')
def createUser():
    """
    This function deals with the creation of new accounts.
    """
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        # If POST request, get the form data.
        email = request.form['E-mail']
        password = request.form['password']
        # Check if given email is associated with an address.
        user = session.query(User).filter_by(email=email)
        try: 
            user = user.one()
            return render_template('newuser.html', uniqueName=False)
        except NoResultFound, e:
            pass
        # Get a salted hash of the password given.
        salt = urandom(16)
        hashed = hashlib.sha256(password+salt)
        # Create a new user and insert it into the database.
        newUser = MenuItem(
            id=id,
            name=request.form['name'],
            sha256_password=hashed,
            salt=salt,
            email=request.form['e-mail'])
        session.add(newUser)
        session.commit()
        # Render the account page for this user.
        return redirect(url_for('myAccount', user=email))
    elif request.method == 'GET':
        # If GET request, render a new user form.
        return render_template('newuser.html')
    return render_template('error.html')

@app.route('/')
@app.route('/hello')
@app.route('/index')
def Index():
    """
    Render a default landing page for these routes.
    """
    return render_template('index.html')

@app.route('/cuisine/new/')
def newCuisine():
    """
    Handles inserting a new cuisine type into the database.
    """
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        # TODO
        return 
    elif request.method == 'GET':
        # If a GET request, just render a login form.
        return render_template("formcuisine.html")
    return render_template("error.html")


@app.route('/cuisine/<int:cuisine_id>/view')
def cuisineDishes(cuisine_id):
    """
    Finds the associated cuisine_id and then rends a page
    with all of the dishes associated with it.
    """
    # Search for the cuisine-id.
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id)
    try: 
        cuisine = cuisine.one()
    except NoResultFound, e:
        return render_template('notfound.html')
    # Get all the dishes associated with the id.
    dishes = session.query(FoodItem).filter_by(cuisine_id=cuisine.id)
    return render_template('viewcuisine.html', dishes=dishes)


@app.route('/cuisine/<int:cuisine_id>/delete')
def deleteCuisine(restaurant_id, menu_id):
    """
    Deletes a cuisine associated with the cuisine-id.
    """
    # Search for the cuisine-id.
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id)
    try: 
        cuisine = cuisine.one()
        # TODO: Confirmation
        # TODO: Delete this id from database, CASCADE
        return render_template('deletecuisine.html')
    except NoResultFound, e:
        return render_template('error.html')


@app.route('/cuisine/<int:cuisine_id>/new')
def newDish(cuisine_id):
    """
    Add a new dish to the database, associated with a cuisine-id.
    """
    # Search the database for the cuisine-id.
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id)
    try: 
        cuisine = cuisine.one()
    except NoResultFound, e:
        # No entry matching the cuisine-id found, render an error page.
        return render_template('error.html')
    # If found, check the HTTP request type.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        # TODO
        return 
    elif request.method == 'GET':
        # If a GET request, just render a form.
        return render_template('formdish.html', cuisine_id=cuisine_id)
        


@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/edit')
def editDish(cuisine_id, dish_id):
    """
    Edit the details of a dish in the database.
    """
    # Search the databae for the given dish.
    _dish = session.query(Dishes).filter_by(id=dish_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != cuisine_id:
            return render_template('error.html')
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        return render_template('error.html')
    
    # If found, check the HTTP request type.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        # TODO
        return 
    elif request.method == 'GET':
        # If a GET request, just render a form.
        return render_template(
            "formdish.html", 
            cuisine_id=cuisine_id,
            dish=_dish)
    else:
        return render_template("error.html")


@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/delete')
def deleteDish(cuisine_id, dish_id):
    """
    This function will deal with deleting a dish from the database.
    """
    _dish = session.query(Dishes).filter_by(id=dish_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != cuisine_id:
            return render_template("error.html")
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        return render_template("error.html")
    
    # If found, check the HTTP request type.
    if request.method == 'POST':
        # If a POST request, extract the form data.
        # TODO
        return 
    elif request.method == 'GET':
        # If a GET request, just render a form.
        return render_template(
            "deletedish.html", 
            cuisine_id=cuisine_id,
            dish=_dish)
    else:
        return render_template("error.html")


@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/view')
def viewDish(cuisine_id, dish_id):
    """
    This function will deal with deleting a dish from the database.
    """
    _dish = session.query(Dishes).filter_by(id=dish_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != cuisine_id:
            return render_template("error.html")
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        return render_template("error.html")
    
    # If found, check the HTTP request type.
    if request.method == 'GET':
        return render_template(
            "viewdish.html", 
            cuisine_id=cuisine_id,
            dish=_dish)
    else:
        return render_template("error.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

