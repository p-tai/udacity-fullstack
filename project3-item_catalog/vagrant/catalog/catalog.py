"""
Main python file that performs url routing and get/post responses.
"""

from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Cuisine, FoodItem

engine = create_engine('sqlite://cookbook.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def HelloWorld():
	return "Hello World"


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
