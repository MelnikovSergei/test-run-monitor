import unittest
from src.utils.project import Project


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project()

    def test_get_project_path(self):
        self.assertIsNone(self.project.get_path())
        
       
        
        
        
        

if __name__ == '__main__':
    unittest.main()
