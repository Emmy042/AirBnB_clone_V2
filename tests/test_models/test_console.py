#!/usr/bin/python3
"""Unit tests for the console create command using FileStorage"""

import os
import unittest
from io import StringIO
import sys
from console import HBNBCommand
from models import storage
from models.state import State

class TestConsoleCreateFileStorage(unittest.TestCase):
    """Tests for `create` with parameters using FileStorage"""

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "file", "FileStorage only")
    def setUp(self):
        """Redirect stdout and clean storage"""
        self.console = HBNBCommand()
        self._stdout = sys.stdout
        sys.stdout = StringIO()
        storage._FileStorage__objects.clear()

    def tearDown(self):
        """Restore stdout and clean up"""
        sys.stdout = self._stdout
        storage._FileStorage__objects.clear()

    def test_create_state_with_param(self):
        """Test creating State with name param"""
        self.console.onecmd('create State name="California_is_big"')
        obj_id = sys.stdout.getvalue().strip()
        key = f"State.{obj_id}"
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, "California is big")

    def test_create_with_int_and_str(self):
        """Test mixed param types"""
        self.console.onecmd('create State name="New_York" level=5')
        obj_id = sys.stdout.getvalue().strip()
        key = f"State.{obj_id}"
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, "New York")
        self.assertEqual(obj.level, 5)


if __name__ == '__main__':
    unittest.main()
