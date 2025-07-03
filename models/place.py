#!/usr/bin/python3
""" Place Module for HBNB project """

import models
from os import getenv
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id', ondelete='CASCADE'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id', ondelete='CASCADE'),
                             primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """A place to stay"""
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete, delete-orphan"
        )

        from models.amenity import Amenity
        from models.place import place_amenity  # must import after Amenity

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            backref="place_amenities"
        )

    else:
        amenity_ids = []

        @property
        def reviews(self):
            """Returns list of Review instances with place_id equal to self.id"""
            from models.review import Review
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns list of Amenity instances linked by amenity_ids."""
            from models.amenity import Amenity
            return [amenity for amenity in models.storage.all(Amenity).values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Append only Amenity objects to amenity_ids."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
