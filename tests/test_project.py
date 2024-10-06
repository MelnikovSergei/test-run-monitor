import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.project import Project


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project()
        self.project.add_test_suite("basic_suite")
        self.project.add_test_suite("advanced_suite")
        self.custom_path_project = Project('custom')

    def test_get_project_path(self):
        self.assertIsNone(self.project.get_path())
        
    def test_set_project_path(self):
        self.project.path = 'test'
        self.assertEqual(self.project.get_path(), 'test')
        
    def test_get_custom_project_path(self):
        self.assertEqual(self.custom_path_project.get_path(), 'custom')
     
    def test_run_test_suite_happy_path_basic_suite(self):
        """Act: Run the basic test suite."""
        # Act
        self.project.run_test_suite("basic_suite")
        # Assert: No exception should be raised

    def test_run_test_suite_happy_path_advanced_suite(self):
        """Act: Run the advanced test suite."""
        # Act
        self.project.run_test_suite("advanced_suite")
        # Assert: No exception should be raised
          
    def test_add_test_suite(self):
        self.project.add_test_suite("test")
        self.assertEqual(self.project.test_suites["test"]["status"], "not run")
        self.assertEqual(self.project.test_suites["test"]["last_result"], "")
        self.assertEqual(self.project.test_suites["test"]["execution_time"], "")
        
    def test_get_suites_statuses(self):
        self.assertEqual(self.project.get_suites_statuses(), ["not run", "not run"])
        
    
if __name__ == '__main__':
    unittest.main(start_dir='tests')
