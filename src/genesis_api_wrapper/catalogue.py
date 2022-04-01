import datetime
import typing

from . import enums, tools


class CatalogueAPIWrapper:
    """Methods for listing objects"""

    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new Wrapper containing functions for listing different object types

        :param username: The username which will be used for authenticating at the database. Due
            to constraints of the database the username needs to be exactly 10 characters long and
            may not contain any whitespaces
        :type username: str
        :param password: The password which will be used for authenticating at the database. Due
            to constraints of the database the password needs to be at least 10 characters long,
            may not exceed 20 characters and may not contain any whitespaces
        :type password: str
        :param language: The language in which the responses are returned by the database.
            :py:enum:mem:`~genesis_api_wrapper.enums.Language.GERMAN` has the most compatibility
            with the database
            since most of the tables are on German. Therefore, this parameter defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.Language.GERMAN`
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

    async def cubes(
        self,
        object_name: str,
        storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """
        **PREMIUM ACCESS REQUIRED**

        List the datacubes matching the ``object_name``

        :param object_name: The identifier code of the data cubes. The usage of an asterisk
            (``*``) is permitted as wildcard
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage, optional
        :param result_count: The maximal amount of results which are returned by the database,
            defaults to 100
        :type result_count: int, optional
        :return: The response from the database parsed into a dict. If the ``Content-Type``
            header indicated a non-JSON response the response is stored in a temporary file and
            the file path will be returned
        :rtype: dict, os.PathLike
        :raises exceptions.GENESISPermissionError: The supplied account does not have the
            permissions to access data cubes.
        :raises ValueError: One of the parameters does not contain a valid value. Please check
            the message of the exception for further information
        """
        if " " in object_name:
            raise ValueError("The object_name parameter may not contain whitespaces")
        if len(object_name) == 0:
            raise ValueError("The object_name parameter may not be empty")
        if len(object_name) > 10:
            raise ValueError("The object_name parameter may not exceed 10 characters")
        if type(storage_location) is not enums.ObjectStorage:
            raise ValueError(
                f"The storage_location parameter only accepts "
                f"{repr(enums.ObjectStorage)} values"
            )
        if result_count < 1:
            raise ValueError("The result_count parameter value may not be below 0")
        if result_count > 2500:
            raise ValueError("The result_count parameter value may not exceed 2500")
        query_parameters = self._base_parameter | {
            "selection": object_name,
            "area": storage_location.value,
            "pagelength": result_count,
        }
        query_path = self._service_url + "/cubes"
        return await tools.get_database_response(query_path, query_parameters)

    async def cubes2statistic(
        self,
        object_name: str,
        cube_code: typing.Optional[str] = None,
        storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """
        **PREMIUM ACCESS REQUIRED**

        List the datacubes matching the ``object_name``

        :param object_name: The identifier code of the statistic
        :type object_name: str
        :param cube_code: The identifier code of the cube. The usage of an asterisk
            (``*``) is permitted as wildcard. This value acts as filter, only showing the data
            cubes matching this code
        :type cube_code: str, optional
        :param storage_location: The storage location of the object, defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :param result_count: The maximal amount of results which are returned by the database,
            defaults to 100
        :type result_count: int
        :return: The response from the database parsed into a dict. If the ``Content-Type``
            header indicated a non-JSON response the response is stored in a temporary file and
            the file path will be returned
        :rtype: dict, os.PathLike
        :raises exceptions.GENESISPermissionError: The supplied account does not have the
            permissions to access data cubes.
        :raises ValueError: One of the parameters does not contain a valid value. Please check
            the message of the exception for further information
        """
        if " " in object_name:
            raise ValueError("The object_name parameter may not contain whitespaces")
        if "*" in object_name:
            raise ValueError(
                "The object_name parameter may not contain asterisks. Wildcards are "
                "not permitted"
            )
        if len(object_name) == 0:
            raise ValueError("The object_name parameter may not be empty")
        if len(object_name) > 6:
            raise ValueError("The object_name parameter may not exceed 6 characters")
        if cube_code is not None and " " in cube_code:
            raise ValueError("The cube_code parameter may not contain whitespaces")
        if cube_code is not None and len(cube_code) == 0:
            raise ValueError("The cube_code parameter may not be empty")
        if cube_code is not None and len(cube_code) > 10:
            raise ValueError("The cube_code parameter may not exceed 10 characters")
        if type(storage_location) is not enums.ObjectStorage:
            raise ValueError(
                f"The storage_location parameter only accepts "
                f"{repr(enums.ObjectStorage)} values"
            )
        if result_count < 1:
            raise ValueError("The result_count parameter value may not be below 0")
        if result_count > 2500:
            raise ValueError("The result_count parameter value may not exceed 2500")
        query_parameters = self._base_parameter | {
            "name": object_name,
            "selection": "" if cube_code is None else cube_code,
            "area": storage_location.value,
            "pagelength": result_count,
        }
        query_path = self._service_url + "/cubes2statistic"
        return await tools.get_database_response(query_path, query_parameters)

    async def cubes2variable(
        self,
        object_name: str,
        cube_code: str,
        storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """
        **PREMIUM ACCESS REQUIRED**

        List the datacubes matching the ``object_name``

        :param object_name: The identifier code of the variable
        :type object_name: str
        :param cube_code: The identifier code of the cube. The usage of an asterisk
            (``*``) is permitted as wildcard. This value acts as filter, only showing the
            data cubes matching this code
        :type cube_code: str, optional
        :param storage_location: The storage location of the object, defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :param result_count: The maximal amount of results which are returned by the
        database,
            defaults to 100
        :type result_count: int
        :return: The response from the database parsed into a dict. If the ``Content-Type``
            header indicated a non-JSON response the response is stored in a temporary
            file and
            the file path will be returned
        :rtype: dict, os.PathLike
        :raises exceptions.GENESISPermissionError: The supplied account does not have the
            permissions to access data cubes.
        :raises ValueError: One of the parameters does not contain a valid value. Please check
            the message of the exception for further information
        """
        if " " in object_name:
            raise ValueError("The object_name parameter may not contain whitespaces")
        if "*" in object_name:
            raise ValueError(
                "The object_name parameter may not contain asterisks. Wildcards are "
                "not permitted"
            )
        if len(object_name) == 0:
            raise ValueError("The object_name parameter may not be empty")
        if len(object_name) > 6:
            raise ValueError("The object_name parameter may not exceed 6 characters")
        if cube_code is not None and " " in cube_code:
            raise ValueError("The cube_code parameter may not contain whitespaces")
        if cube_code is not None and len(cube_code) == 0:
            raise ValueError("The cube_code parameter may not be empty")
        if cube_code is not None and len(cube_code) > 10:
            raise ValueError("The cube_code parameter may not exceed 10 characters")
        if type(storage_location) is not enums.ObjectStorage:
            raise ValueError(
                f"The storage_location parameter only accepts "
                f"{repr(enums.ObjectStorage)} values"
            )
        if result_count < 1:
            raise ValueError("The result_count parameter value may not be below 0")
        if result_count > 2500:
            raise ValueError("The result_count parameter value may not exceed 2500")
        query_parameters = self._base_parameter | {
            "name":       object_name,
            "selection":  "" if cube_code is None else cube_code,
            "area":       storage_location.value,
            "pagelength": result_count,
        }
        query_path = self._service_url + "/cubes2variable"
        return await tools.get_database_response(query_path, query_parameters)

    async def jobs(
            self,
            object_name: str,
            search_by: enums.JobCriteria,
            sort_by: enums.JobCriteria,
            job_type: enums.JobType = enums.JobType.ALL,
            result_count: int = 100,
    ) -> dict:
        """
        Get a list of the jobs that match the parameters
        
        :param object_name: The identifier code of the job. The usage of an asterisk
            (``*``) is permitted as wildcard. This value acts as filter, only showing the
            jobs matching this code
        :type object_name: str
        :param search_by: Criteria which shall be applied to the object_name
        :type search_by: enums.JobCriteria
        :param sort_by: Criteria by which the output shall be sorted
        :type sort_by: enums.JobCriteria
        :param job_type: The type of jobs which shall be returned, defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.JobType.ALL`
        :type job_type: enums.JobType
        :param result_count: The maximal amount of results which are returned by the
            database, defaults to 100
        :type result_count: int
        :rtype: dict, os.PathLike
        :raises exceptions.GENESISPermissionError: The supplied account does not have the
            permissions to this resource.
        :raises ValueError: One of the parameters does not contain a valid value. Please check
            the message of the exception for further information
        """
        if " " in object_name:
            raise ValueError("The object_name parameter may not contain whitespaces")
        if "*" in object_name:
            raise ValueError(
                "The object_name parameter may not contain asterisks. Wildcards are "
                "not permitted"
            )
        if len(object_name) == 0:
            raise ValueError("The object_name parameter may not be empty")
        if len(object_name) > 50:
            raise ValueError("The object_name parameter may not exceed 50 characters")
        if type(search_by) is not enums.JobCriteria:
            raise ValueError(
                f"The search_by parameter only accepts values from the following enumeration: "
                f"{repr(enums.JobCriteria)}"
            )
        if type(sort_by) is not enums.JobCriteria:
            raise ValueError(
                f"The sort_by parameter only accepts values from the following enumeration: "
                f"{repr(enums.JobCriteria)}"
            )
        if type(job_type) is not enums.JobType:
            raise ValueError(
                f"The job_type parameter only accepts values from the following enumeration: "
                f"{repr(enums.JobType)}"
            )
        if result_count < 1:
            raise ValueError("The result_count parameter value may not be below 0")
        if result_count > 2500:
            raise ValueError("The result_count parameter value may not exceed 2500")
        query_parameter = self._base_parameter | {
            'selection': object_name,
            'searchcriterion': search_by.value,
            'sortcriterion': sort_by.value,
            'type': job_type.value,
            'pagelength': result_count
        }
        query_path = self._service_url + '/jobs'
        return await tools.get_database_response(query_path, query_parameter)
        
    async def modified_data(
            self,
            object_filter: str,
            object_type: enums.ObjectType = enums.ObjectType.ALL,
            updated_after: datetime.date = datetime.date.today() - datetime.timedelta(days=-7),
            result_count: int = 100
    ) -> dict:
        """
        **Due to an error in the database the parameter** ``result_count`` **is ignored by the
        database**
        
        Get a list of modified objects which were modified or uploaded after ``updated_after``.
        The following objects are returned by this query:
            - Tables
            - Statistics
            - Statistic updates
        
        :param object_filter: The identifier code of the object. The usage of an asterisk
            (``*``) is permitted as wildcard. This value acts as filter, only showing the
            jobs matching this code
        :type object_filter: str
        :param object_type: The type of object that shall be listed
            Allowed types (enums):
                - :py:enum:mem:`~genesis_api_wrapper.enums.ObjectType.ALL`
                - :py:enum:mem:`~genesis_api_wrapper.enums.ObjectType.TABLES`
                - :py:enum:mem:`~genesis_api_wrapper.enums.ObjectType.STATISTICS`
                - :py:enum:mem:`~genesis_api_wrapper.enums.ObjectType.STATISTIC_UPDATE`
                
        :type object_type: enums.ObjectType
        :param updated_after: The date after which the object needs to be modified or uploaded to
            be returned by the database, defaults to 7 days before today
        :type updated_after: datetime.date
        :param result_count: The number of results that will be returned
        :type result_count: int
        """
        if " " in object_filter:
            raise ValueError("The object_filter parameter may not contain whitespaces")
        if len(object_filter) == 0:
            raise ValueError("The object_filter parameter may not be empty")
        if len(object_filter) > 50:
            raise ValueError("The object_filter parameter may not exceed 50 characters")
        if type(object_type) is not enums.ObjectType:
            raise ValueError(
                f"The object_type parameter only accepts values from the following enumeration: "
                f"{repr(enums.ObjectType)}"
            )
        if object_type not in [enums.ObjectType.ALL, enums.ObjectType.TABLES,
                               enums.ObjectType.STATISTICS, enums.ObjectType.STATISTICS_UPDATE]:
            raise ValueError(
                f"The supplied object_type ({object_type}) is not allowed at this resource"
            )
        if updated_after > datetime.date.today():
            raise ValueError(
                f'The updated_after parameter is in the future'
            )
        # ==== Build the query data ====
        query_path = self._service_url + '/modifieddata'
        query_parameters = self._base_parameter | {
            'selection': object_filter,
            'type': object_type.value,
            'date': tools.convert_date_to_string(updated_after),
            'pagelength': result_count
        }
        # ==== Return the query data ====
        return await tools.get_database_response(query_path, query_parameters)

    async def quality_signs(self) -> dict:
        """
        Get the list of quality signs from the database
        
        :return: The Response containing the quality signs present in the database
        :rtype: dict
        """
        query_path = self._service_url + '/qualitysigns'
        query_parameters = self._base_parameter
        return await tools.get_database_response(query_path, query_parameters)

    async def results(
            self,
            object_name: str,
            storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
            result_count: int = 100
    ) -> dict:
        """
        Get a list of result tables matching the ``object_name``

        :param object_name: The identifier code of the result tables. The usage of an asterisk
            (``*``) is permitted as wildcard
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
            :py:enum:mem:`~genesis_api_wrapper.enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage, optional
        :param result_count: The maximal amount of results which are returned by the database,
            defaults to 100
        :type result_count: int, optional
        :return: The response from the database parsed into a dict. If the ``Content-Type``
            header indicated a non-JSON response the response is stored in a temporary file and
            the file path will be returned
        :rtype: dict, os.PathLike
        :raises exceptions.GENESISPermissionError: The supplied account does not have the
            permissions to access data cubes.
        :raises ValueError: One of the parameters does not contain a valid value. Please check
            the message of the exception for further information
        """
        if " " in object_name:
            raise ValueError("The object_name parameter may not contain whitespaces")
        if len(object_name) == 0:
            raise ValueError("The object_name parameter may not be empty")
        if len(object_name) > 10:
            raise ValueError("The object_name parameter may not exceed 10 characters")
        if type(storage_location) is not enums.ObjectStorage:
            raise ValueError(
                f"The storage_location parameter only accepts "
                f"{repr(enums.ObjectStorage)} values"
            )
        if result_count < 1:
            raise ValueError("The result_count parameter value may not be below 0")
        if result_count > 2500:
            raise ValueError("The result_count parameter value may not exceed 2500")
        # ==== Build the query path and parameters ====
        query_path = self._service_url + '/results'
        query_parameters = self._base_parameter | {
            'selection': object_name,
            'area': storage_location.value,
            'pagelength': result_count
        }
        # ==== Get the response ====
        return await tools.get_database_response(query_path, query_parameters)

    async def statistics(
        self,
        selector: str = None,
        search_by: enums.StatisticCriteria = enums.StatisticCriteria.CODE,
        sort_by: enums.StatisticCriteria = enums.StatisticCriteria.CODE,
        result_count: int = 100,
    ) -> dict:
        """Get a list of statistics matching the supplied parameters

        :param selector: The filter which is applied to the field selected by `search_by`
        :type selector: str
        :param search_by: The field on which the selector shall be applied to, defaults to
            `GENESISenums.StatisticCriteria.Code`
        :type search_by: enums.StatisticCriteria
        :param sort_by: Sort the results by the field, defaults to
            `GENESISenums.StatisticCriteria.Code`
        :type sort_by: enums.StatisticCriteria
        :param result_count: The number of results that shall be returned
        :type result_count: int
        :return: The response from the database
        :rtype: dict
        """
        # Check if the selector matches the required constraints
        if (selector is not None) and not (1 <= len(selector.strip()) <= 15):
            raise ValueError("The selector's length needs to be between 1 and 15")
        _param = self._base_parameter | {
            "selection": "" if selector is None else selector,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/statistics"
        return await tools.get_database_response(_url, _param)

    async def statistics2variable(
        self,
        variable_name: str,
        statistic_selector: str = None,
        search_by: enums.StatisticCriteria = enums.StatisticCriteria.CODE,
        sort_by: enums.StatisticCriteria = enums.StatisticCriteria.CODE,
        object_area: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ):
        """Get a list of statistics which are referenced by the selected variable

        :param variable_name: The name of the variable [required]
        :type variable_name: str
        :param statistic_selector: Filter for the statistics by the code of them, [optional,
            stars allowed to wildcard, max. length 15]
        :type statistic_selector: str
        :param search_by: The field on which the code shall be applied, [optional, defaults
            to `GENESISenums.StatisticCriteria.CODE`]
        :type search_by: enums.StatisticCriteria
        :param sort_by: The field by which the results are to be sorted, [optional, defaults
            to `GENESISenums.StatisticCriteria.CODE`]
        :type sort_by: enums.StatisticCriteria
        :param object_area: The area in which the object is stored
        :type object_area: enums.ObjectStorage
        :param result_count: The number of results which are returned by the request
        :type result_count: int
        :return: The response returned by the server
        """
        if variable_name is None:
            raise ValueError("The variable name needs to be set to run a successful query")
        if not 1 <= len(variable_name.strip()) <= 15:
            raise ValueError("The variable names length needs to be between 1 and 15 signs")
        if statistic_selector and not (1 <= len(statistic_selector.strip()) <= 15):
            raise ValueError("The selectors length may not exceed 15 characters")
        # Create the parameters object
        _param = self._base_parameter | {
            "name": variable_name,
            "selection": "" if statistic_selector is None else statistic_selector,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "pagelength": result_count,
            "area": object_area.value,
        }
        _url = self._service_url + "/statistics2variable"
        return await tools.get_database_response(_url, _param)

    async def tables(
        self,
        table_selector: str,
        object_area: enums.ObjectStorage = enums.ObjectStorage.ALL,
        sort_by: enums.TableCriteria = enums.TableCriteria.CODE,
        result_count: int = 100,
    ) -> dict:
        """Get a list of tables matching the selector from the selected object area

        :param table_selector: The code of the table [required, stars (*) allowed for wildcards]
        :param object_area: The area in which the table is stored [defaults to ALL]
        :param sort_by: The criteria by which the results shall be sorted [defaults to CODE]
        :param result_count: The number of results that shall be returned
        :return: A list of tables matching the request
        """
        if table_selector and not (1 <= len(table_selector.strip()) <= 15):
            raise ValueError(
                "The table selector needs to be at least 1 character and max 15 " "characters"
            )
        _param = self._base_parameter | {
            "selection": table_selector,
            "area": object_area.value,
            "searchcriterion": "Code",
            "sortcriterion": sort_by.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/tables"
        return await tools.get_database_response(_url, _param)

    async def tables2statistics(
        self,
        statistics_name: str,
        table_selector: str = None,
        object_area: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of tables matching the table selector which are assigned to the

        :param statistics_name: Name of the statistic [required, 1-15 characters]
        :param table_selector: Filter for the tables code [optional, wildcards allowed]
        :param object_area: The location of the statistic/tables
        :param result_count: The number of tables in the response
        :return:
        """
        if statistics_name is None:
            raise ValueError("The name of the statistic is required to get the tables")
        if not 1 <= len(statistics_name.strip()) <= 15:
            raise ValueError("The length of the statistics name needs to be between 1 and 15")
        if table_selector and not (1 <= len(table_selector.strip()) <= 15):
            raise ValueError(
                "The table selector needs to be at least 1 character and max 15 " "characters"
            )
        _param = self._base_parameter | {
            "name": statistics_name,
            "selection": table_selector,
            "area": object_area.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/tables2statistic"
        return await tools.get_database_response(_url, _param)

    async def tables2variable(
        self,
        variable_name: str,
        table_selector: str = None,
        object_area: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of tables matching the table selector which are assigned to the

        :param variable_name: Name of the statistic [required, 1-15 characters]
        :param table_selector: Filter for the tables code [optional, wildcards allowed]
        :param object_area: The location of the statistic/tables
        :param result_count: The number of tables in the response
        :return:
        """
        if variable_name is None:
            raise ValueError("The name of the statistic is required to get the tables")
        if not 1 <= len(variable_name) <= 15:
            raise ValueError("The length of the statistics name needs to be between 1 and 15")
        if table_selector and not (1 <= len(table_selector.strip()) <= 15):
            raise ValueError(
                "The table selector needs to be at least 1 character and max 15 " "characters"
            )
        _param = self._base_parameter | {
            "name": variable_name,
            "selection": table_selector,
            "area": object_area.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/tables2variable"
        return await tools.get_database_response(_url, _param)

    async def terms(self, term_selector: str, result_count: int = 100):
        """Get a list of terms according to the selector

        :param term_selector: The selector for the terms [required, wildcards allowed]
        :param result_count: The number of terms which shall be returned
        :return: The parsed response from the server
        """
        if term_selector is None:
            raise ValueError("The selector for the terms is a required parameter")
        if not 1 <= len(term_selector.strip()) <= 15:
            raise ValueError("The length of the selector needs to be between 1 and 15")
        _param = self._base_parameter | {"selection": term_selector, "pagelength": result_count}
        _url = self._service_url + "/terms"
        return await tools.get_database_response(_url, _param)

    async def timeseries(
        self,
        timeseries_selector: str,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of timeseries according to the selector and the location of the object

        :param timeseries_selector: The selector for the timeseries [required, wildcards
            allowed]
        :param object_location: The area in which the object is stored [default:
            ``enums.ObjectStorage.ALL``]
        :param result_count: The number of results that shall be returned
        :return: The list of found timeseries
        """
        if timeseries_selector is None:
            raise ValueError("The selector is required for a successful database request")
        if not 1 <= len(timeseries_selector.strip()) <= 15:
            raise ValueError(
                "The length of the selector needs to be between 1 and 15 " "characters"
            )
        _param = self._base_parameter | {
            "selection": timeseries_selector,
            "area": object_location.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/timeseries"
        return await tools.get_database_response(_url, _param)

    async def timeseries2statistic(
        self,
        statistic_name: str,
        timeseries_selector: typing.Optional[str] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ):
        """Get a list of timeseries which are related to the selected statistic

        :param statistic_name: Code of the statistic [required, length: 1-15 characters]
        :param timeseries_selector: Filter for the timeseries by their code [optional,
            wildcards allowed]
        :param object_location: The storage location of the object
        :param result_count: The number of results that shall be returned
        :return: A response containing the list of timeseries which match the supplied
            parameters
        """
        if statistic_name is None:
            raise ValueError("The name of the statistic is a required parameter")
        if timeseries_selector and not (1 <= len(timeseries_selector.strip()) <= 15):
            raise ValueError(
                "If a timeseries_selector is supplied its length may not exceed " "15 characters"
            )
        # Build the query parameters
        param = self._base_parameter | {
            "name": statistic_name,
            "selection": "" if timeseries_selector is None else timeseries_selector,
            "area": object_location.value,
            "pagelength": result_count,
        }
        url = self._service_url + "/timeseries2statistic"
        return await tools.get_database_response(url, param)

    async def timeseries2variable(
        self,
        variable_name: str,
        timeseries_selector: typing.Optional[str] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of timeseries which are related to the specified variable

        :param variable_name: The code of the variable [required]
        :param timeseries_selector: A filter for the returned timeseries [optional, wildcards
            allowed]
        :param object_location: The storage location in which the search shall be executed [
            optional, defaults to ``enums.ObjectStorage.ALL``]
        :param result_count: The number of results that shall be returned
        :return: A parsed response containing the list of timeseries, if any were found
        """
        if variable_name is None:
            raise ValueError("The variable_name is a required parameter")
        if not (1 <= len(variable_name.strip()) <= 15):
            raise ValueError("The length of the variable name may not exceed 15 characters")
        if timeseries_selector and not (1 <= len(timeseries_selector.strip()) <= 15):
            raise ValueError(
                "If a timeseries_selector is supplied its length may not exceed " "15 characters"
            )
        # Build the query parameters
        _query_parameter = self._base_parameter | {
            "name": variable_name,
            "selection": "" if timeseries_selector is None else timeseries_selector,
            "area": object_location.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/timeseries2variable"
        return await tools.get_database_response(_url, _query_parameter)

    async def values(
        self,
        value_filter: str,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        search_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        sort_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        result_count: int = 100,
    ) -> dict:
        """Get a list of values specified by the filter

        :param value_filter: The filter for the value identifications [optional, wildcards
            allowed]
        :param object_location: The storage location which shall be used during the search [
            optional, defaults to ``GenericCriteria.CODE``]
        :param search_by: The criteria which is used in combination to the value_filter [
            optional, defaults to ``GenericCriteria.CODE``]
        :param sort_by: The criteria by which the results are sorted [optional, defaults to
            ``GenericCriteria.CODE``]
        :param result_count: The number of results returned
        :return: A parsed response containing the list of values
        """
        # Check the received variables
        if value_filter is None:
            raise ValueError("The value_filter is a required parameter")
        if not 1 <= len(value_filter.strip()) <= 15:
            raise ValueError(
                "The length of the value_filter needs to be at least 1 character "
                "and may not exceed 15 characters"
            )
        if not 1 <= result_count <= 2500:
            raise ValueError(
                "The number of results returned needs to be greater than 1, "
                "but may not exceed 2500"
            )
        # Build the query parameters
        params = self._base_parameter | {
            "selection": value_filter,
            "area": object_location.value,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "pagelength": result_count,
        }
        _url = self._service_url + "/values"
        return await tools.get_database_response(_url, params)

    async def values2variable(
        self,
        variable_name: str,
        value_filter: typing.Optional[str] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        search_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        sort_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        result_count: int = 100,
    ) -> dict:
        """Get a list of characteristic values for the supplied variable

        :param variable_name: The code of the variable
        :param value_filter: A filter for the returned values [optional, wildcards allowed]
        :param object_location: The storage location of the variable
        :param search_by: Criteria which is applied to the ``value_filter``
        :param sort_by: Criteria which is used to sort the results
        :param result_count: The number of characteristic values which may be returned
        :return: A parsed response from the server containing the list of characteristic values
        """
        # Check if the variable name is set correctly
        if not variable_name or len(variable_name.strip()) == 0:
            raise ValueError("The variable_name is a required parameter and may not be empty")
        if not (1 <= len(variable_name.strip()) <= 15):
            raise ValueError(
                "The length of the variable_name may not exceed 15 characters "
                "and may not be below 1 character"
            )
        if "*" in variable_name:
            raise ValueError("The variable_name may not contain any wildcards (*)")
        # Check the value filter
        if value_filter and not (1 <= len(value_filter.strip()) <= 15):
            raise ValueError(
                "The length of the value_filter may not exceed 15 characters and "
                "may not be below 1"
            )
        # Check the number of results returned
        if not 1 <= result_count <= 2500:
            raise ValueError(
                "The number of results returned needs to be greater than 1, "
                "but may not exceed 2500"
            )
        # Create the query parameter
        _param = self._base_parameter | {
            "name": variable_name,
            "selection": value_filter,
            "area": object_location.value,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "pagelength": result_count,
        }
        # Build the url for the call
        _url = self._service_url + "/values2variable"
        # Make the call and await the response
        return await tools.get_database_response(_url, _param)

    async def variables(
        self,
        variable_filter: str,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        search_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        sort_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        variable_type: enums.VariableType = enums.VariableType.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of variables matching the filter and object location

        :param variable_filter: Identification Code of the variable [required, wildcards
          allowed]
        :param object_location: The storage location of the object [optional]
        :param search_by: Criteria which is applied to the variable filter [optional]
        :param sort_by: Criteria by which the result is sorted [optional]
        :param variable_type: The type of variable [optional]
        :param result_count: The number of results that may be returned [optional]
        :return: A parsed response from the server containing the variables
        """
        # Check if the filter is supplied correctly
        if not variable_filter or len(variable_filter.strip()) == 0:
            raise ValueError("The variable_filter is a required parameter any may not be empty")
        if not (1 <= len(variable_filter.strip()) <= 6):
            raise ValueError("The variable_filter may only contain up to 6 characters")
        # Check if the result count is set properly
        if not (1 <= result_count <= 2500):
            raise ValueError("The number of possible results needs to be between 1 and 2500")
        # Build the query parameters
        _param = self._base_parameter | {
            "selection": variable_filter,
            "area": object_location.value,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "type": variable_type.value,
            "pagelength": result_count,
        }
        # Build the url
        _url = self._service_url + "/variables"
        # Return the parsed result
        return await tools.get_database_response(_url, _param)

    async def variables2statistic(
        self,
        statistic_name: str,
        variable_filter: typing.Optional[str] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        search_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        sort_by: enums.GenericCriteria = enums.GenericCriteria.CODE,
        variable_type: enums.VariableType = enums.VariableType.ALL,
        result_count: int = 100,
    ) -> dict:
        """Get a list of variables related to the supplied statistic

        :param statistic_name: The identification of the statistic [required]
        :param variable_filter: Filter for the returned variables [optional, wildcards allowed]
        :param object_location: Storage location which is used for the search [optional]
        :param search_by: Criteria which is applied to the variable_filter [optional]
        :param sort_by: Criteria specifying how the results are to be sorted [optional]
        :param variable_type: The type of variables that shall be returned [optional]
        :param result_count: Max. amount of results returned by the server [optional]
        :return: A parsed response containing a list of variables
        """
        # Check if the statistic_name is set correctly
        if not statistic_name or len(statistic_name.strip()) == 0:
            raise ValueError("The statistic_name is a required parameter")
        if not (1 <= len(statistic_name.strip()) <= 15):
            raise ValueError("The length of statistic_name may not exceed 15 characters")
        if "*" in statistic_name:
            raise ValueError("The statistic_name may not contain wildcards (*)")
        # Check if the variable_filter is set correctly if set
        if variable_filter and not (1 <= len(variable_filter.strip()) <= 6):
            raise ValueError(
                "The variable_filter may not exceed the length of 6 characters, "
                "if it is supplied"
            )
        # Build the query parameters
        _param = self._base_parameter | {
            "name": statistic_name,
            "selection": variable_filter,
            "area": object_location.value,
            "searchcriterion": search_by.value,
            "sortcriterion": sort_by.value,
            "type": variable_type.value,
            "pagelength": result_count,
        }
        # Build the query path
        _path = self._service_url + "/variables2statistic"
        return await tools.get_database_response(_path, _param)
