"""
Database setup script.
Holds the table definitions for the item_catalog project.
"""

import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey,\
						Integer, String, DateTime, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
    __tablename__ = "users" 
    
    email = Column(String(100), primary_key=True)
    sha256_password = Column(String(256), nullable=False)
    salt = Column(String(20))


class Cuisine(Base):
    __tablename__ = "cuisine"

    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)


class Dishes(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    cuisine = relationship(Cuisine)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
    owner = relationship(Users)
    owner_id = Column(String(100), ForeignKey('users.email'))
    creation_time = Column(DateTime, default=datetime.datetime.utcnow)
    edit_time = Column(DateTime, default=datetime.datetime.utcnow)
    image = Column(Binary)
    
    @property
    def serialize(self):
		# Returns object data in serializable format
		return {
			'id' : self.id,
			'name' : self.name,
			'description' : self.description,
			'cuisine_id' : self.cuisine_id,
			'owner' : self.owner_id
		}


engine = create_engine('sqlite:///cuisines.db')
Base.metadata.create_all(engine)
