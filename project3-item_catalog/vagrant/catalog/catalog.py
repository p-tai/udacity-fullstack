"""
Main python file that performs url routing and get/post responses.
"""

from flask import Flask, render_template, url_for,\
                  request, flash, Session, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from catalog_db_setup import Base, Cuisine, Dishes, Users

engine = create_engine('sqlite:///cookbook.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from os import urandom
from base64 import b64encode

import hashlib

@app.route('/login/', methods=['GET','POST'])
def userLogin():
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
            flash("Error: E-mail/password combination not found. " +\
                  "Please try again.")
            return render_template('loginform.html', bad_account=True)

        # Compare hash of password+salt to stored hash value.
        hashed = hashlib.sha256(password+cuisine.salt)
        if cuisine.sha256_password == hashed:

            # Login user.
            login_user(email)
            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            if not next_is_valid(next):
                return flask.abort(400)

            return redirect(url_for('myAccount'))
        else:
            # Password doesn't match, render login-form.
            flash("Error: E-mail/password combination not found. " +\
                  "Please try again.")
            return render_template('loginform.html')
    else:
        # If a GET request, just render a login form.
        return render_template('loginform.html')

        
@app.route("/logout")
def userLogout():
    return redirect(url_for(index))

@app.route('/createuser/', methods=['GET','POST'])
def createUser():
    """
    This function deals with the creation of new accounts.
    """
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        # If POST request, get the form data.
        _email = request.form['e-mail']
        _email = _email.encode('utf-8')
        _password = request.form['password']
        _password = _password.encode('utf-8')
        # Check if given email is associated with an address.
        user = session.query(Users).filter_by(email=_email)
        try: 
            user = user.one()
            flash("A user with that e-mail address already exists.")
            return render_template('testform.html')
        except NoResultFound, e:
            pass
        except OperationalError, e:
            pass
        # Get a salted hash of the password given.
        _salt = urandom(16)
        _salt = b64encode(_salt)
        hashed = hashlib.sha256(_password+_salt).hexdigest()
        hashed = hashed.encode('UTF-8')
        # Create a new user and insert it into the database.
        newUser = Users(
            email = _email,
            sha256_password = hashed,
            salt = _salt)
        session.add(newUser)
        session.commit()
        print newUser.email, newUser.sha256_password, _password
        # Render the account page for this user.
        flash("User account successfully created.")
        return render_template('createuser.html')
        return #redirect(url_for('myAccount', user=email))
    else:
        # If GET request, render a new user form.
        return render_template('createuser.html')

@app.route("/account")
def viewAccount():
    return render_template('account.html')

@app.route('/')
@app.route('/index')
def index():
    """
    Render a default landing page for these routes.
    """
    return render_template('index.html')

@app.route('/cuisine/new/', methods=['GET','POST'])
# @app.route('/cuisine/new/<string:name>')
def newCuisine():
    """
    Handles inserting a new cuisine type into the database.
    """
    # Check if the HTTP request given is a POST or GET request.
    print(request.method)
    if request.method == 'POST':
        # If a POST request, extract the form data.
        _name = request.form['name']
        cuisine = session.query(Cuisine).filter_by(name = _name.lower())
        try: 
            cuisine = cuisine.one()
            flash(u'%s cuisine not added: Cuisine already exists' % _name)
            return render_template("formcuisine.html", cu_id=cuisine.id)
        except NoResultFound, e:
            pass
        flash(u'%s cuisine successfully added' % _name)
        # Create a new Cuisine tuple and add it to the Database.
        newCuisine = Cuisine(name=_name.lower())
        session.add(newCuisine)
        session.commit()
        return render_template("formcuisine.html", cu_id=newCuisine.id)
    else:
        # If a GET request, just render a login form.
        return render_template("formcuisine.html")


@app.route('/cuisine/<int:c_id>/view')
def viewCuisine(c_id):
    """
    Finds the associated cuisine_id and then rends a page
    with all of the dishes associated with it.
    """
    # Search for the cuisine-id.
    cuisine = session.query(Cuisine).filter_by(id=c_id)
    try: 
        cuisine = cuisine.one()
    except NoResultFound, e:
        return render_template('notfound.html')
    # Get all the dishes associated with the id.
    dishes = session.query(Dishes).filter_by(cuisine_id=c_id)
    try:
        dishes = dishes.all()
    except NoResultFound, e:
        dishes=None
    return render_template('viewcuisine.html', 
                            dishes=dishes, 
                            cuisine=cuisine)


@app.route('/cuisine/<int:c_id>/delete')
def deleteCuisine(c_id):
    """
    Deletes a cuisine associated with the cuisine-id.
    """
    # Search for the cuisine-id.
    cuisine = session.query(Cuisine).filter_by(id=c_id)
    try: 
        cuisine = cuisine.one()
        session.delete(cuisine)
        session.commit()
    except NoResultFound, e:
        return render_template('cuisinedelete.html', cuisine=None)
    return render_template('cuisinedelete.html', cuisine=cuisine.name)

# TO DO
@app.route('/cuisine/<int:c_id>/new', methods=['GET','POST'])
def newDish(c_id):
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
        return render_template('dishform.html', cuisine_id=cuisine_id)
        

# TO DO
@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/edit', methods=['GET','POST'])
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

# TO DO
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

# TO DO
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

@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/view/JSON')
def viewDishJSON(cuisine_id, dish_id):
    _dish = session.query(Dishes).filter_by(id=dish_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != cuisine_id:
            return jsonify ({})
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        return render_template("error.html")
    return jsonify(dish=[_dish.serialize])


if __name__ == "__main__":
    app.debug = True
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SECRET_KEY"] = "a_Secret_Key"
    _flask_session = Session()
    app.run(host='0.0.0.0', port=5000)
