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
    __tablename__ = "cuisine"

    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    

class Dishes(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
    cuisine = relationship(Cuisine)
    owner_id = Column(String(100), ForeignKey('Users'))
    owner = relationship(Users)
    
    @property
    def serialize(self):
		# Returns object data in serializable format
		return {
			'id' : self.id,
			'name' : self.name,
			'description' : self.description,
			'cuisine' : self.cuisine
			'owner' : self.owner_id
		}
    

class Users(Base):
    __tablename__ = "users" 
    
    email = Column(String(100), primary_key=True)
    sha256_password = Column(String(256), nullable=False)
    salt = Column(String(20))


engine = create_engine('sqlite:///cookbook.db')
Base.metadata.create_all(engine)
