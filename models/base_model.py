#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models
from os import getenv
import sqlalchemy
import uuid

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        date = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("created_at"):
                kwargs["created_at"] = datetime.strptime(
                         kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at"):
                kwargs["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            if not self.id:
                self.id = str(uuid.uuid4())
                for key, value in kwargs.items():
                    if "__class__" not in key:
                        setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        auxDict = {}
        auxDict.update(self.__dict__)
        try:
            del auxDict['_sa_instance_state']
        except Exception:
            pass
        auxDict.update({'__class__':
            (str(type(self)).split('.')[-1]).split('\'')[0]})
        auxDict['created_at'] = self.created_at.isoformat()
        auxDict['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in auxDict:
            del auxDict["_sa_instance_state"]
        return auxDict

    def delete(self):
        """delete"""
        from models import storage
        storage.delete(self)
