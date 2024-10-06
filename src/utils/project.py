class Project:
    """
    A class representing a project.
    """

    def __init__(self, path=None):
        """
        Initializes a new instance of the Project class.

        Parameters
        ----------
        path : str
            The path to the project directory.
        """

        self.path = path
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
        return [self.test_suites[suite]["status"] for suite in self.test_suites]

    def run_test_suite(self, suite_name: str) -> None:
        pass

    def add_test_suite(self, suite_name: str) -> None:
        self.test_suites[suite_name] = {
            "status": "not run",
            "last_result": "",
            "execution_time": "",
        }
