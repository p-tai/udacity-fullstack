"""
Main python file that performs url routing and get/post responses.
"""

from flask import Flask, render_template, url_for, request,\
                  redirect, flash, jsonify, abort

from flask import Session as login_session

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from catalog_db_setup import Base, Cuisine, Dishes, Users

engine = create_engine('sqlite:///cuisines.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from os import urandom
from base64 import b64encode

import hashlib
import datetime

def correctCasing(str):
    """
    Forces given str to a standard Capitalization where
    all the first letters of a word are capitalized.
    """
    strings = str.split(' ')
    strings = [s[0].upper()+s[1:].lower() for s in strings]
    return ' '.join(strings)
        

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# TO DO
@app.route('/login/', methods=['GET','POST'])
def userLogin():
    """
    This function deals with user login.
    """
    state = ''.join(b64encode(urandom(32)).decode('utf-8'))
    _flask_session['state'] = state
    return state
    # Check if the HTTP request given is a POST or GET request.
    if request.method == 'POST':
        return render_template('loginform.html')
    else:
        # If a GET request, just render a login form.
        return render_template('loginform.html')

# TO DO
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
            return render_template('createuser.html')
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
    cuisineList = session.query(Cuisine).all()
    recentDishes = session.query(Dishes).order_by(Dishes.creation_time).limit(5).all()
    
    return render_template('index.html',
                            cuisines = cuisineList,
                            dishes=recentDishes)


@app.route('/cuisine/new/', methods=['GET','POST'])
def newCuisine():
    """
    Handles inserting a new cuisine type into the database.
    """
    # Check if the HTTP request given is a POST or GET request.
    print(request.method)
    if request.method == 'POST':
        # If a POST request, extract the form data.
        _name = request.form['name']
        _name = correctCasing(_name)
        cuisine = session.query(Cuisine).filter_by(name = _name)
        try: 
            cuisine = cuisine.one()
            flash(u'\"%s\" not added. Cuisine already exists.' % _name)
            return render_template("formcuisine.html", cu_id=cuisine.id)
        except NoResultFound, e:
            pass
        # Create a new Cuisine tuple and add it to the Database.
        newCuisine = Cuisine(name=_name)
        session.add(newCuisine)
        session.commit()
        flash(u'%s cuisine successfully added.' % _name)
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
        abort(404)
    # Get all the dishes associated with the id.
    dishes = session.query(Dishes).filter_by(cuisine_id=c_id)
    try:
        dishes = dishes.all()
    except NoResultFound, e:
        dishes=None
    return render_template('viewcuisine.html', 
                            dishes=dishes, 
                            cuisine=cuisine)


@app.route('/cuisine/<int:c_id>/delete', methods=['GET','POST'])
def deleteCuisine(c_id):
    """
    Deletes a cuisine associated with the cuisine-id.
    """
    # Search for the cuisine-id.
    _cuisine = session.query(Cuisine).filter_by(id=c_id)
    try: 
        _cuisine = _cuisine.one()
        if request.method == 'POST':
            session.delete(_cuisine)
            session.commit()
            flash(u'\"%s\" deleted.' % _cuisine.name)
            return redirect(url_for('index'))
    except NoResultFound, e:
        abort(404)
    return render_template('cuisinedelete.html', cuisine=_cuisine)

# TO DO
@app.route('/cuisine/<int:c_id>/new', methods=['GET','POST'])
def newDish(c_id):
    """
    Add a new dish to the database, associated with a cuisine-id.
    """
    # Search the database for the cuisine-id.
    _cuisine = session.query(Cuisine).filter_by(id=c_id)
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
        try: 
            _dish = _dish.one()
            # Dish already exists in database, do not add to db.
            flash(u'%s has previously been submitted.' % _name)
            return render_template('dishform.html', 
                                    cuisine_id=c_id, 
                                    dish_id=_dish.id)
        except NoResultFound, e:
            pass
        newDish = Dishes(name=_name, 
                        description=_desc, 
                        cuisine=_cuisine,
                        cuisine_id=_cuisine.id,
                        creation_time = datetime.datetime.utcnow)
        session.add(newDish)
        session.commit()
        flash(u'%s dish successfully added.' % _name)
        return render_template('dishform.html', 
                                cuisine_id=c_id, 
                                dish_id=newDish.id)
    elif request.method == 'GET':
        # If a GET request, just render a form.
        return render_template('dishform.html', 
                                cuisine_id=c_id)
        


@app.route('/cuisine/<int:c_id>/<int:d_id>/edit', methods=['GET','POST'])
def editDish(c_id, d_id):
    """
    Edit the details of a dish in the database.
    """
    # Search the databae for the given dish.
    _dish = session.query(Dishes).filter_by(id=d_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != c_id:
            abort(404)
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        abort(404)
    
    # If found, check the HTTP request type.
    if request.method == 'POST':
        
        # If a POST request, extract the form data.
        _name = request.form['name']
        _desc = request.form['description']
        
        # Check the name was changed
        if(_name == ""):
            _name = _dish.name
        
        else: 
            # Make sure a dish with this name doesn't already exist.
            _name = correctCasing(_name)
            try: 
                temp = _dish
                _dish = session.query(Dishes).filter_by(name=_name).one()
                # Dish already exists in database, do not add to db.
                flash(u'%s already exists. Edit failed.' % _name)
                return render_template('dishedit.html', 
                                        cuisine_id=c_id, 
                                        dish=temp)
            except NoResultFound, e:
                pass
        # Update the dish's details in the database.
        _dish.name = _name
        if(_desc != ""):
            _dish.description = _desc
        _dish.edit_time=datetime.datetime.utcnow
        session.commit()
        
        # Notify the front-end that the update was successful.
        flash(u'%s successfully updated.' % _name)
        return render_template('dishedit.html', 
                                cuisine_id=c_id,
                                dish=_dish)
    else:
        # If a GET request, just render a blank form.
        return render_template('dishedit.html', 
                                cuisine_id=c_id,
                                dish=_dish)


@app.route('/cuisine/<int:c_id>/<int:d_id>/delete', methods=['GET','POST'])
def deleteDish(c_id, d_id):
    """
    This function will deal with deleting a dish from the database.
    """
    # First check the dish exists.
    _dish = session.query(Dishes).filter_by(id=d_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine_id != c_id:
            abort(404)
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        abort(404)
    if request.method == 'POST':
        # Post request results in deleting the dish from the db.
        session.delete(_dish)
        session.commit()
        flash(u'\"%s\" deleted.' % _dish.name)
        return redirect(url_for('index'))
    else:
        # Get request results in a confirmation check.
        return render_template('dishdelete.html', 
                                cuisine_id=_dish.cuisine_id,
                                dish=_dish)


@app.route('/cuisine/<int:c_id>/<int:d_id>/view')
def viewDish(c_id, d_id):
    
    """
    This function will deal with listing a dish's details.
    """
    # Search the databae for the given dish.
    _dish = session.query(Dishes).filter_by(id=d_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != c_id:
            abort(404)
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        abort(404)
    return render_template("dishview.html", 
                            cuisine_id=c_id,
                            dish=_dish)
    
    

@app.route('/cuisine/<int:c_id>/<int:d_id>/view/JSON')
def viewDishJSON(c_id, d_id):
    _dish = session.query(Dishes).filter_by(id=d_id)
    try: 
        _dish = _dish.one()
        # Also check that the cuisine-id is correct.
        if _dish.cuisine.id != c_id:
            return jsonify ([{}])
    except NoResultFound, e:
        # No entry matching the dish-id found, render an error page.
        abort(404)
    return jsonify(dish=[_dish.serialize])


if __name__ == "__main__":
    app.debug = True
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SECRET_KEY"] = "a_Secret_Key"
    _flask_session = login_session()
    app.run(host='0.0.0.0', port=5000)
