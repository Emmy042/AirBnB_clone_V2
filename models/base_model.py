#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()



class BaseModel:
    """A base class for all hbnb models"""
    
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, *args, **kwargs):
        
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            if '__class__' in kwargs:
                del kwargs['__class__']
            
            # Explicitly create instance attributes from kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)
                        
            self.__dict__.update(kwargs)
            if 'id' not in self.__dict__:
                self.id = str(uuid.uuid4())
            if 'created_at' not in self.__dict__:
                self.created_at = datetime.now()
            if 'updated_at' not in self.__dict__:
                self.updated_at = datetime.now()

            


    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                      (str(type(self)).split('.')[-1]).split('\'')[0]})
    
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        else:
            dictionary['created_at'] = self.created_at

        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        else:
            dictionary['updated_at'] = self.updated_at

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']

        return dictionary

    
    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)

