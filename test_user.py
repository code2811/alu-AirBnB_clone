#!/usr/bin/python3
import unittest
from models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_instance(self):
        self.assertIsInstance(self.user, User)

    def test_attributes(self):
        self.user.first_name = "Alice"
        self.user.last_name = "Doe"
        self.user.email = "alice@example.com"
        self.assertEqual(self.user.first_name, "Alice")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "alice@example.com")

if __name__ == '__main__':
    unittest.main()

