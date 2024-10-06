import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.project import Project


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project()

    def test_get_project_path(self):
        self.assertIsNone(self.project.get_path())
        
    def test_set_project_path(self):
        self.project.path = 'test'
        self.assertEqual(self.project.get_path(), 'test')
        
        

if __name__ == '__main__':
    unittest.main(start_dir='src/tests')
