#!/usr/bin/python3
"""This module instantiates the storage system and loads all models"""

from os import getenv

# Force import of all model classes so SQLAlchemy registers them
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

# Determine which storage engine to use
storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
