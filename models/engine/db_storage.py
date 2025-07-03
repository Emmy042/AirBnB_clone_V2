# models/engine/db_storage.py

from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# Get database credentials from environment variables
user = os.getenv("HBNB_MYSQL_USER")
pwd = os.getenv("HBNB_MYSQL_PWD")
host = os.getenv("HBNB_MYSQL_HOST", "localhost")  # default to localhost
db = os.getenv("HBNB_MYSQL_DB")

class DBStorage:
    """database storage for HBNB"""
    __engine = None
    __session = None
    
    def __init__(self):
        self.__engine = create_engine(
        f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True
        )
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls=None):
        """Query all objects or objects of a specific class from the database"""
        obj_dict = {}

        # Import models
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        if cls:
            # Query specific class
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
        else:
            # Query all types
            classes = [User, State, City, Amenity, Place, Review]
            for clz in classes:
                objs = self.__session.query(clz).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dict[key] = obj

        return obj_dict
    
    def new(self, obj):
        self.__session.add(obj)
        
    def save(self):
        self.__session.commit()
        
    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
            
    def reload(self):
        """Create all tables and initialize session"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        

