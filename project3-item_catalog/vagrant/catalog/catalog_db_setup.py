"""
Database setup script.
Holds the table definitions for the item_catalog project.
"""

import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey,\
                       Integer, String, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    """
    User table
    id:     primary key, auto-incremented int
    email:  email of the user
    name:   name of the user
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    name = Column(String(100))


class Cuisines(Base):
    """
    Cuisines table
    id:         primary key, auto-incremented int
    name:       name of the cuisine
    owner:      owner entity that created this cuisine
    owner_id:   id of the owner associated with this cuisine
    """
    __tablename__ = "cuisines"

    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    owner = relationship(Users)
    owner_id = Column(Integer, ForeignKey('users.id'))

    @property
    def serialize(self):
        # Returns object data in serializable format.
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id
        }


class Dishes(Base):
    """
    Dishes table
    id:             primary key, auto-incremented int
    name:           name of the dish
    description:    short string describing the dish
    cuisine:        cuisine entity associated with this dish
    cuisine_id:     id of the cuisine associated with this dish
    owner:          owner entity that created this cuisine
    owner_id:       id of the owner associated with this cuisine
    creation_time:  the time a row was inserted
    edit_time:      the time a row was last edited
    image_path:     location of the image stored locally
    """
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    cuisine = relationship(Cuisines,
                           cascade="all, delete-orphan",
                           single_parent=True)
    cuisine_id = Column(Integer, ForeignKey('cuisines.id'))
    owner = relationship(Users)
    owner_id = Column(Integer, ForeignKey('users.id'))
    creation_time = Column(DateTime, default=datetime.datetime.utcnow)
    edit_time = Column(DateTime, default=datetime.datetime.utcnow)
    image_path = Column(String(100))

    @property
    def serialize(self):
        # Returns object data in serializable format.
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creation_time': self.creation_time,
            'cuisine_id': self.cuisine_id,
            'owner_id': self.owner_id
        }


engine = create_engine('sqlite:///cuisines.db')
Base.metadata.create_all(engine)
