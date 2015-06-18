"""
Main python file that performs url routing and get/post responses.
"""

from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Cuisine, Dishes, Users

engine = create_engine('sqlite:///cookbook.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from os import random

import hashlib

@app.route('/login/')
def userLogin(username, password):
	"""
	This function deals with user login.
	"""
    if request.method == 'POST':
		email = request.form['E-mail']
		password = request.form['password']
		user = session.query(User).filter_by(email=email)
		try: 
			user = user.one()
		except NoResultFound, e:
			#username not found
			return #render_template('login.html', bad_account=True)
		hashed = hashlib.sha256(password+cuisine.salt)
		if cuisine.sha256_password == hashed:
			#password matches
			#login(username)
			return #redirect(url_for('myAccount', user=username)
		else:
			#password does not match
			return #render_template('login.html', bad_account=True)
    elif request.method == 'GET':
        return render_template('login.html', bad_account=False)

@app.route('/createuser/')
def createUser():
	"""
	This function deals with the creation of new accounts
	"""
	if request.method == 'POST':
		email = request.form['E-mail']
		user = session.query(User).filter_by(email=email).one()
		if user:
			return render_template('newuser.html', uniqueName=False)
		password = request.form['password']
		salt = urandom(16)
		hashed = hashlib.sha256(password+salt)
        newUser = MenuItem(
			id=id,
            name=request.form['name'],
            sha256_password=hashed,
            salt=salt,
            email=request.form['e-mail'])
        session.add(newUser)
        session.commit()
        return redirect(url_for('myAccount', user=email))
    elif request.method == 'GET':
        return render_template('newuser.html')

@app.route('/')
@app.route('/hello')
@app.route('/index')
def Index():
	return render_template('index.html')

@app.route('/cuisine/new/')
def newCuisine():
    return "page to create a new cuisine type"


@app.route('/cuisine/<int:cuisine_id>/')
def cuisineDishes(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    dishes = session.query(FoodItem).filter_by(cuisine_id=cuisine.id)
    return "todo"


@app.route('/cuisine/<int:cuisine_id>/delete')
def deleteCuisine(restaurant_id, menu_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    return "page to delete a cuisine type"


@app.route('/cuisine/<int:cuisine_id>/new')
def newDish(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    return "page to create a new dish type"


@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/edit')
def editDish(cuisine_id, dish_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    dishes = session.query(FoodItem).filter_by(cuisine_id=restaurant.id)
    if not dishes:
        return None
    return "page to edit a dish"


@app.route('/cuisine/<int:cuisine_id>/<int:dish_id>/delete')
def deleteDish(cuisine_id, dish_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    dishes = session.query(FoodItem).filter_by(cuisine_id=restaurant.id)
    if not dishes:
        return None
    return "page to delete a menu item. Task 3 complete!"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

