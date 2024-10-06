

class Project:
    """
    A class representing a project.
    """

    def __init__(self, path = None):
        """
        Initializes a new instance of the Project class.

        Parameters
        ----------
        path : str
            The path to the project directory.
        """
        
        self.path = path
        
    def get_path(self):
        """
        Returns the path to the project directory.

        Returns
        -------
        str
            The path to the project directory.
        """
        
        return self.path
    