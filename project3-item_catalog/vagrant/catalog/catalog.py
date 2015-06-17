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

@app.route('/login/')
def userLogin():
    """TODO"""
    pass

@app.route('/createuser/')
def createUser():
    """TODO"""

@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

@app.route('/cuisine/<int:cuisine_id>/')
def cuisineDishes(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if not cuisine:
        return None
    dishes = session.query(FoodItem).filter_by(cuisine_id=cuisine.id)
    return "todo"


@app.route('/cuisine/new/')
def newCuisine():
    return "page to create a new cuisine type"


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
