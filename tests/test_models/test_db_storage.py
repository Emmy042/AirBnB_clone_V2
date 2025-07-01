#!/usr/bin/python3


import unittest
import os
from models.engine.db_storage import DBStorage
from models import storage
from models.state import State

@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage only")
class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up a test instance of DBStorage"""
        self.storage = DBStorage()
        self.storage.reload()

    def test_new_and_save(self):
        """Test that new() adds and save() commits an object"""
        new_state = State(name="Lagos")
        self.storage.new(new_state)
        self.storage.save()
        key = f"State.{new_state.id}"
        self.assertIn(key, self.storage.all(State))
