#!/usr/bin/python3

import os
import MySQLdb
import unittest
from console import HBNBCommand

class TestConsoleDBStorage(unittest.TestCase):
    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DB storage only")
    def test_create_state_db(self):
        """Test that 'create State name=California' adds row to DB"""
        self.console = HBNBCommand()
        db = MySQLdb.connect(user="hbnb_test", passwd="hbnb_test_pwd",
                             host="localhost", db="hbnb_test_db")
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM states;")
        before = cursor.fetchone()[0]

        self.console.onecmd('create State name="California"')

        cursor.execute("SELECT COUNT(*) FROM states;")
        after = cursor.fetchone()[0]

        self.assertEqual(after, before + 1)
        db.close()
