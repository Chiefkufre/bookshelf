#Import all dependencies
import unittest
import json
from models import setup_db
from __init__ import create_app, Book



class BookTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "4321thoiP$", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)
        
    
    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/books')

        self.assertEqual(res.status_code, 200)
        

if __name__ == "__main__":
    unittest.main()