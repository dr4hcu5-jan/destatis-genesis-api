from . import tools, enums


class FindAPIWrapper:
    """Methods for searching for objects"""

    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new FindAPIWrapper section method wrapper

        :param username: The username which will be used for authenticating at the database. Due
            to constraints of the database the username needs to be exactly 10 characters long and
            may not contain any whitespaces
        :type username: str
        :param password: The password which will be used for authenticating at the database. Due
            to constraints of the database the password needs to be at least 10 characters long,
            may not exceed 20 characters and may not contain any whitespaces
        :type password: str
        :param language: The language in which the responses are returned by the database.
            :py:enum:mem:`~enums.Language.GERMAN` has the most compatibility with the database
            since most of the tables are on German. Therefore, this parameter defaults to
            :py:enum:mem:`~enums.Language.GERMAN`
        :type language: enums.Language
        :raise ValueError: The username or the password did not match the constraints stated in
            their description.
        """
        if " " in username:
            raise ValueError("The username may not contain any whitespaces")
        if len(username) != 10:
            raise ValueError("The username may only be 10 characters long")
        if " " in password:
            raise ValueError("The password may not contain any whitespaces")
        if len(password) < 10:
            raise ValueError(
                f"The password may not be shorter than 10 characters. Current "
                f"length: {len(password)}"
            )
        if len(password) > 20:
            raise ValueError(
                f"The password may not be longer that 20 characters. Current "
                f"length: {len(password)}"
            )
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
