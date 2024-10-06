class Project:
    """
    A class representing a project.
    """

    def __init__(self, name=None):
        """
        Initializes a new instance of the Project class.

        Parameters
        ----------
        path : str
            The path to the project directory.
        """

        self.path = name
        self.test_suites = {}

    def get_path(self) -> str:
        """
        Returns the path to the project directory.

        Returns
        -------
        str
            The path to the project directory.
        """

        return self.path

    def get_suites_statuses(self) -> list:
        """
        Returns the status of each test suite in the project.

        Returns
        -------
        list
            The status of each test suite in the project.
        """
        
        return [self.test_suites[suite]["status"] for suite in self.test_suites]
    
    def get_suite_status(self, suite_name: str) -> str:
        """
        Returns the status of a test suite in the project.

        Parameters
        ----------
        suite_name : str
            The name of the test suite.

        Returns
        -------
        str
            The status of the test suite.
        """
        
        if suite_name in self.test_suites:
            return self.test_suites[suite_name]["status"]
        else:
            return "Suite not found"
    def run_test_suite(self, suite_name: str) -> None:
        
        pass

    def add_test_suite(self, suite_name: str) -> None:
        """
        Adds a new test suite to the project.

        Parameters
        ----------
        suite_name : str
            The name of the new test suite.
        """
        
        self.test_suites[suite_name] = {
            "status": "not run",
            "last_result": "",
            "execution_time": "",
        }
