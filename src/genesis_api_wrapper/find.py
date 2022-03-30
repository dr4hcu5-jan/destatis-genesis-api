from . import tools, enums


class FindAPIWrapper:
    """Methods for searching for objects"""

    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new FindAPIWrapper section method wrapper

        :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: str
        :param language: The language which should be used in the response bodies, defaults to
            German
        :type language: enums.Language, optional
        """
        # Check if the username consists of 10 characters
        if len(username) != 10:
            raise ValueError("The username is not 10 characters long.")
        # Check if the password's length is between 10 and 20 characters
        if not (10 <= len(password) <= 20):
            raise ValueError("The password is not between 10 and 20 characters long")
        # Since all values passed the check save the username and password to the wrapper,
        # but keep them private
        self._username = username
        self._password = password
        self._language = language
        self._service_url = "/catalogue"
        self._base_parameter = {
            "username": self._username,
            "password": self._password,
            "language": self._language.value,
        }

    async def find(
        self,
        search_term: str,
        category: enums.ObjectType = enums.ObjectType.ALL,
        results_per_category: int = 100,
    ) -> dict:
        """Get a list of objects in the specified category which match the search term

        :param search_term: Term for which the search is executed
        :param category: The category in which the search is executed
        :param results_per_category: Number of results per category
        :return: A response containing the results of the search
        """
        _params = self._base_parameter | {
            "term": search_term,
            "category": category.value,
            "pagelength": str(results_per_category),
        }
        return await tools.get_database_response("/find/find", _params)
