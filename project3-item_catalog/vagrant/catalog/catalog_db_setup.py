"""
Database setup script.
Holds the table definitions for the item_catalog project.
"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Cuisine(Base):
	
	__tablename__ == "cuisine"
	
	id = Column(integer, primary_key=True)
	name = Column(String(63), nullable=False)
	

class FoodItem(Base):
	__tablename__ == "dishes"
	
	id = Column(integer, primary_key=True)
	name = Column(String(100), nullable=False)
	description = Column(String(250))
	cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
	cuisine = relationship(Cuisine)
	

engine = create_engine('sqlite:///cookbook.db')
Base.metadata.create_all(engine)
