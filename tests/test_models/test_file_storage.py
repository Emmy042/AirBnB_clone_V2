#!/usr/bin/python3


import unittest
import os
from models.engine.file_storage import FileStorage
from models import storage
from models.state import State

@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage only")
class TestFileStorage(unittest.TestCase):
    def setUp(self):
        """Create a test instance of FileStorage"""
        self.storage = FileStorage()
        self.storage.reload()

    def test_all_returns_dict(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_and_save(self):
        """Test that new() adds and save() writes an object"""
        new_state = State(name="Abuja")
        self.storage.new(new_state)
        self.storage.save()
        key = f"State.{new_state.id}"
        self.assertIn(key, self.storage.all())
