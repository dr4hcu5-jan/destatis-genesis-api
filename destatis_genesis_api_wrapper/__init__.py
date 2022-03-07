"""Wrapper for the JSON API of the DESTATIS GENESIS database"""
import logging

from pydantic import SecretStr

from . import tools
from .enums import GENESISLanguage, GENESISCategory, GENESISJobType, GENESISJobCriteria, \
    GENESISObjectType, GENESISStatisticCriteria, GENESISArea, GENESISTableCriteria, \
    GENESISValueCriteria, GENESISVariableCriteria, GENESISVariableType
from .responses import *

# Create a logger for the whole module
logger = logging.getLogger('DESTATIS-GENESIS')
"""The logger which is used in this module"""


class AsyncGENESISWrapper:
    """
    An asynchronous Wrapper for the GENESIS API
    """

    def __init__(
            self,
            username: str,
            password: str,
            language: GENESISLanguage = GENESISLanguage.GERMAN
    ):
        """Create a new GENESIS database wrapper

        :param username: The username which was assigned during the creation of an account(
            length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: SecretStr
        :param language: The language which should be used in the response bodies, defaults to
            German
        :type language: GENESISLanguage
        """
        # Check if the username consists of 10 characters
        if len(username) != 10:
            raise ValueError("The username is not 10 characters long.")
        # Check if the password's length is between 10 and 20 characters
        if not (10 <= len(password) <= 20):
            raise ValueError("The password is not between 10 and 20 characters long")
        # Since all values passed the check save the username and password to the wrapper,
        # but keep them private
        self.__username = username
        self.__password = SecretStr(password)
        self.__language = language
        self.__base_parameter = {
            'username': self.__username,
            'password': self.__password.get_secret_value(),
            'language': self.__language.value
        }
        self.hello_world: AsyncGENESISWrapper.__HelloWorld = self.__HelloWorld(username, password, language)
        """Methods in the `Hello World` part of the official API documentation"""
        self.find: AsyncGENESISWrapper.__Find = self.__Find(username, password, language)
        """Methods in the `Find` part of the official API documentation"""
        self.catalogue: AsyncGENESISWrapper.__Catalogue = self.__Catalogue(username, password, language)
        """Methods in the `Catalogue` part of the official API documentation"""
    
    class __HelloWorld:
        """All methods from the HelloWorld section of the API documentation"""

        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new HelloWorld method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self._password = SecretStr(password)
            self._language = language
            self._service_url = '/catalogue'
            self._base_parameter = {
                'username': self._username,
                'password': self._password.get_secret_value(),
                'language': self._language.value
            }
        
        @staticmethod
        async def who_am_i() -> HelloWorld.WhoAmIResponse:
            """Get information about the client data transmitted to the GENESIS database
            
            :return: A Response containing the IP Address and the User-Agent for the request that
            has
                been executed
            :rtype: WhoAmIResponse
            """
            return await tools.get_parsed_response('/helloworld/whoami', None,
                                                   HelloWorld.WhoAmIResponse)
    
        async def login_check(self) -> HelloWorld.LoginCheckResponse:
            """Check the login data which were supplied during the creation of the wrapper
            
            :return: The response from the server containing the success or failure of the reqeust
            :rtype: LoginCheckResponse
            """
            return await tools.get_parsed_response(
                '/helloworld/logincheck',
                self._base_parameter,
                HelloWorld.LoginCheckResponse
            )
    
    class __Find:
        """Methods for searching for objects"""
    
        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new Find section method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self._password = SecretStr(password)
            self._language = language
            self._service_url = '/catalogue'
            self._base_parameter = {
                'username': self._username,
                'password': self._password.get_secret_value(),
                'language': self._language.value
            }
    
        async def find(
                self,
                search_term: str,
                category: GENESISCategory = GENESISCategory.ALL,
                results_per_category: int = 100
        ) -> Find.FindResult:
            """Get a list of objects in the specified category which match the search term
            
            :param search_term: Term for which the search is executed
            :param category: The category in which the search is executed
            :param results_per_category: Number of results per category
            :return: A response containing the results of the search
            """
            _params = self._base_parameter | {
                'term':       search_term,
                'category':   category.value,
                'pagelength': str(results_per_category)
            }
            return await tools.get_parsed_response('/find/find', _params, Find.FindResult)
    
    class __Catalogue:
        """Methods for listing objects"""
    
        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new Find section method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self._password = SecretStr(password)
            self._language = language
            self._service_url = '/catalogue'
            self._base_parameter = {
                'username': self._username,
                'password': self._password.get_secret_value(),
                'language': self._language.value
            }
            
        async def cubes(
                self,
                selection: str,
                object_area: GENESISArea = GENESISArea.ALL,
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes matching the selector (PREMIUM ACCOUNTS ONLY)
            
            :param selection: The code of the data cube. You may use a star (*) to allow wild
            carding
            :param object_area: The location of the object
            :param results: The maximum items which are received from the database
            :return: A list of information about the found data cubes
            """
            # TODO: Add check of parameters
            _parameters = self._base_parameter | {
                'selection': selection,
                'area': object_area.value,
                'pagelength': str(results)
            }
            _url = self._service_url + '/cubes'
            return await tools.get_parsed_response(_url, _parameters, Catalogue.CubeResponse)
        
        async def cubes2statistic(
                self,
                statistic_name: constr(min_length=1, max_length=6),
                cube_code: constr(min_length=1, max_length=10),
                object_area: GENESISArea = GENESISArea.ALL,
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes of a statistic matching the selector (PREMIUM ACCOUNTS ONLY)
            
            :param statistic_name: The name of the statistic that shall be used
            :param cube_code: The code of the data cube in this statistic, star based wild-carding
                is allowed
            :param object_area: The area in which the object is stored
            :param results: The number of maximum results that should be pulled
            :return: A list of information about the data cubes
            """
            # TODO: Add check of parameters
            _parameters = self._base_parameter | {
                'name': statistic_name,
                'selection':  cube_code,
                'area': object_area.value,
                'pagelength': str(results)
            }
            _url = self._service_url + '/cubes2statistic'
            return await tools.get_parsed_response(_url, _parameters, Catalogue.CubeResponse)
    
        async def cubes2variable(
                self,
                variable_name: constr(min_length=1, max_length=6),
                cube_code: constr(min_length=1, max_length=10),
                object_area: GENESISArea = GENESISArea.ALL,
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes related to the specified variable
            
            :param variable_name: The name of the variable, (max. 6 character)
            :param cube_code: The code of a cube which is related to the variable, stars (*) may be
                used for wild carding
            :param object_area: The area in which the object is stored
            :param results: Number of results which are retrieved
            :return: A list of the data cubes which are related to the variable
            """
            # TODO: Add check of parameters
            _parameters = self._base_parameter | {
                'name': variable_name,
                'selection': cube_code,
                'area': object_area.value,
                'pagelength': results
            }
            _url = self._service_url + '/cubes2variable'
            return await tools.get_parsed_response(
                _url,
                _parameters,
                Catalogue.CubeResponse
            )
        
        async def jobs(
                self,
                selector: str,
                search_by: GENESISJobCriteria,
                sort_by: GENESISJobCriteria,
                job_type: GENESISJobType = GENESISJobType.ALL,
                results: int = 100
        ) -> Catalogue.JobResponse:
            """Get a list of jobs which were created
            
            :param selector: Filter for the jobs to be displayed. (1-50 characters, stars (*)
                allowed for wildcarding)
            :param search_by: The criteria on which the selector is applied to
            :param sort_by: The criteria by which the result shall be listed
            :param job_type: The type of job which is to be returned
            :param results: The number of results that shall be returned
            :return:
            """
            if not (1 <= len(selector.strip()) <= 50):
                raise ValueError('The length of the selector needs to be between 1 and 50 ('
                                 'inclusive)')
            if None in [search_by, sort_by]:
                raise ValueError('All parameter without a default value need to be set')
            _params = self._base_parameter | {
                'selection': selector,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'type': job_type.value,
            }
            _url = self._service_url + '/jobs'
            return await tools.get_parsed_response(_url, _params, Catalogue.JobResponse)
        
        async def modified_data(
                self,
                selector: Optional[str] = None,
                object_type: GENESISObjectType = GENESISObjectType.ALL,
                updated_after: Optional[date] = None,
                results: int = 100
        ) -> Catalogue.ModifiedDataResponse:
            """Get a list of modified objects
            
            DUE TO AN ERROR IN THE DATABASE THE `results` PARAMETER IS BEING IGNORED
            
            :param selector: Filter for the objects to be displayed. (1-15 characters, stars (*)
                allowed for wildcarding)
            :type selector: str
            :param object_type: The type of object that shall be returned
            :type object_type: GENESISObjectType
            :param updated_after: The date after which the objects needed to be changed to be
                returned, defaults to one week (7 days)
            :type updated_after: date
            :param results: The number of results that should be returned
            """
            # Check the parameters for consistency
            if (selector is not None) and (not (1 <= len(selector.strip()) <= 15)):
                raise ValueError("The selector's length needs to be between 1 and 15 (inclusive)")
            if (updated_after is not None) and not (updated_after < date.today()):
                raise ValueError("The specified date may not be today or in the future")
            if not (0 < results <= 2500):
                raise ValueError('The number of results need to be between 1 and 2500')
            # Build the query parameters
            _param = self._base_parameter | {
                'selection': '' if selector is None else selector,
                'type': GENESISObjectType.ALL.value if object_type is None else object_type.value,
                'date': updated_after.strftime('%d.%m.%Y') if updated_after is not None else None,
                'pagelength': results
            }
            _url = self._service_url + '/modifieddata'
            return await tools.get_parsed_response(_url, _param, Catalogue.ModifiedDataResponse)
        
        async def quality_signs(self) -> Catalogue.QualitySignsResponse:
            """Get a list of the quality signs used in the GENESIS database"""
            _url = self._service_url + '/qualitysigns'
            return await tools.get_parsed_response(
                _url, self._base_parameter, Catalogue.QualitySignsResponse
            )
        
        async def results(
                self,
                selector: str = None,
                result_count: int = 100,
                search_area: GENESISArea = GENESISArea.ALL
        ) -> Catalogue.ResultTableResponse:
            """Get a list of result tables
            
            :param search_area: The area in which the objects are saved
            :param selector: Filter for the result tables code, (1-15 characters, stars(*) allowed)
            :type selector: str
            :param result_count: The number of results which should be returned
            :return: A List of information about the result tables
            """
            if (selector is not None) and (not (1 <= len(selector.strip()) <= 15)):
                raise ValueError("The selector's length needs to be between 1 and 15")
            _param = self._base_parameter | {
                'selection': '' if selector is None else selector,
                'area': search_area.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/results'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.ResultTableResponse
            )
        
        async def statistics(
                self,
                selector: str = None,
                search_by: GENESISStatisticCriteria = GENESISStatisticCriteria.CODE,
                sort_by: GENESISStatisticCriteria = GENESISStatisticCriteria.CODE,
                result_count: int = 100
        ) -> Catalogue.StatisticsResponse:
            """Get a list of statistics matching the supplied parameters
            
            :param selector: The filter which is applied to the field selected by ``search_by``
            :type selector: str
            :param search_by: The field on which the selector shall be applied to, defaults to
                ``GENESISStatisticCriteria.Code``
            :type search_by: GENESISStatisticCriteria
            :param sort_by: Sort the results by the field, defaults to
                ``GENESISStatisticCriteria.Code``
            :type sort_by: GENESISStatisticCriteria
            :param result_count: The number of results that shall be returned
            :type result_count: int
            :return: The response from the database
            :rtype: Catalogue.StatisticsResponse
            """
            # Check if the selector matches the required constraints
            if (selector is not None) and not (1 <= len(selector.strip()) <= 15):
                raise ValueError("The selector's length needs to be between 1 and 15")
            _param = self._base_parameter | {
                'selection': '' if selector is None else selector,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/statistics'
            return await tools.get_parsed_response(_url, _param, Catalogue.StatisticsResponse)
            
        async def statistics2variable(
                self,
                variable_name: str,
                statistic_selector: str = None,
                search_by: GENESISStatisticCriteria = GENESISStatisticCriteria.CODE,
                sort_by: GENESISStatisticCriteria = GENESISStatisticCriteria.CODE,
                object_area: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
        ):
            """Get a list of statistics which are referenced by the selected variable
            
            :param variable_name: The name of the variable [required]
            :type variable_name: str
            :param statistic_selector: Filter for the statistics by the code of them, [optional,
                stars allowed to wildcard, max. length 15]
            :type statistic_selector: str
            :param search_by: The field on which the code shall be applied, [optional, defaults
                to `GENESISStatisticCriteria.CODE`]
            :type search_by: GENESISStatisticCriteria
            :param sort_by: The field by which the results are to be sorted, [optional, defaults
                to `GENESISStatisticCriteria.CODE`]
            :type sort_by: GENESISStatisticCriteria
            :param object_area: The area in which the object is stored
            :type object_area: GENESISArea
            :param result_count: The number of results which are returned by the request
            :type result_count: int
            :return: The response returned by the server
            """
            if variable_name is None:
                raise ValueError('The variable name needs to be set to run a successful query')
            if not 1 <= len(variable_name.strip()) <= 15:
                raise ValueError('The variable names length needs to be between 1 and 15 signs')
            if statistic_selector and not (1 <= len(statistic_selector.strip()) <= 15):
                raise ValueError("The selectors length may not exceed 15 characters")
            # Create the parameters object
            _param = self._base_parameter | {
                'name': variable_name,
                'selection': '' if statistic_selector is None else statistic_selector,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'pagelength': result_count,
                'area': object_area.value
            }
            _url = self._service_url + '/statistics2variable'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.StatisticsResponse
            )
        
        async def tables(
                self,
                table_selector: str,
                object_area: GENESISArea = GENESISArea.ALL,
                sort_by: GENESISTableCriteria = GENESISTableCriteria.CODE,
                result_count: int = 100
        ) -> Catalogue.TableResponse:
            """Get a list of tables matching the selector from the selected object area
            
            :param table_selector: The code of the table [required, stars (*) allowed for wildcards]
            :param object_area: The area in which the table is stored [defaults to ALL]
            :param sort_by: The criteria by which the results shall be sorted [defaults to CODE]
            :param result_count: The number of results that shall be returned
            :return: A list of tables matching the request
            """
            if table_selector and not (1 <= len(table_selector.strip()) <= 15):
                raise ValueError('The table selector needs to be at least 1 character and max 15 '
                                 'characters')
            _param = self._base_parameter | {
                'selection': table_selector,
                'area': object_area.value,
                'searchcriterion': 'Code',
                'sortcriterion': sort_by.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/tables'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.TableResponse
            )
        
        async def tables2statistics(
                self,
                statistics_name: str,
                table_selector: str = None,
                object_area: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
        ) -> Catalogue.TableResponse:
            """Get a list of tables matching the table selector which are assigned to the
            
            :param statistics_name: Name of the statistic [required, 1-15 characters]
            :param table_selector: Filter for the tables code [optional, wildcards allowed]
            :param object_area: The location of the statistic/tables
            :param result_count: The number of tables in the response
            :return:
            """
            if statistics_name is None:
                raise ValueError('The name of the statistic is required to get the tables')
            if not 1 <= len(statistics_name.strip()) <= 15:
                raise ValueError('The length of the statistics name needs to be between 1 and 15')
            if table_selector and not (1 <= len(table_selector.strip()) <= 15):
                raise ValueError('The table selector needs to be at least 1 character and max 15 '
                                 'characters')
            _param = self._base_parameter | {
                'name': statistics_name,
                'selection': table_selector,
                'area': object_area.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/tables2statistic'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.TableResponse
            )

        async def tables2variable(
                self,
                variable_name: str,
                table_selector: str = None,
                object_area: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
        ) -> Catalogue.TableResponse:
            """Get a list of tables matching the table selector which are assigned to the

            :param variable_name: Name of the statistic [required, 1-15 characters]
            :param table_selector: Filter for the tables code [optional, wildcards allowed]
            :param object_area: The location of the statistic/tables
            :param result_count: The number of tables in the response
            :return:
            """
            if variable_name is None:
                raise ValueError('The name of the statistic is required to get the tables')
            if not 1 <= len(variable_name) <= 15:
                raise ValueError('The length of the statistics name needs to be between 1 and 15')
            if table_selector and not (1 <= len(table_selector.strip()) <= 15):
                raise ValueError('The table selector needs to be at least 1 character and max 15 '
                                 'characters')
            _param = self._base_parameter | {
                'name':       variable_name,
                'selection':  table_selector,
                'area':       object_area.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/tables2variable'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.TableResponse
            )
        
        async def terms(
                self,
                term_selector: str,
                result_count: int = 100
        ):
            """Get a list of terms according to the selector
            
            :param term_selector: The selector for the terms [required, wildcards allowed]
            :param result_count: The number of terms which shall be returned
            :return: The parsed response from the server
            """
            if term_selector is None:
                raise ValueError('The selector for the terms is a required parameter')
            if not 1 <= len(term_selector.strip()) <= 15:
                raise ValueError('The length of the selector needs to be between 1 and 15')
            _param = self._base_parameter | {
                'selection': term_selector,
                'pagelength': result_count
            }
            _url = self._service_url + '/terms'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.TermResponse
            )
        
        async def timeseries(
                self,
                timeseries_selector: str,
                object_location: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
        ) -> Catalogue.TimeseriesResponse:
            """Get a list of timeseries according to the selector and the location of the object
            
            :param timeseries_selector: The selector for the timeseries [required, wildcards
                allowed]
            :param object_location: The area in which the object is stored [default:
                ``GENESISArea.ALL``]
            :param result_count: The number of results that shall be returned
            :return: The list of found timeseries
            """
            if timeseries_selector is None:
                raise ValueError('The selector is required for a successful database request')
            if not 1 <= len(timeseries_selector.strip()) <= 15:
                raise ValueError('The length of the selector needs to be between 1 and 15 '
                                 'characters')
            _param = self._base_parameter | {
                'selection': timeseries_selector,
                'area': object_location.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/timeseries'
            return await tools.get_parsed_response(
                _url, _param, Catalogue.TimeseriesResponse
            )

        async def timeseries2statistic(
                self,
                statistic_name: str,
                timeseries_selector: Optional[str] = None,
                object_location: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
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
                raise ValueError("If a timeseries_selector is supplied its length may not exceed "
                                 "15 characters")
            # Build the query parameters
            param = self._base_parameter | {
                'name': statistic_name,
                'selection': "" if timeseries_selector is None else timeseries_selector,
                'area': object_location.value,
                'pagelength': result_count
            }
            url = self._service_url + '/timeseries2statistic'
            return await tools.get_parsed_response(
                url, param, Catalogue.TimeseriesResponse
            )
        
        async def timeseries2variable(
                self,
                variable_name: str,
                timeseries_selector: Optional[str] = None,
                object_location: GENESISArea = GENESISArea.ALL,
                result_count: int = 100
        ) -> Catalogue.TimeseriesResponse:
            """Get a list of timeseries which are related to the specified variable
            
            :param variable_name: The code of the variable [required]
            :param timeseries_selector: A filter for the returned timeseries [optional, wildcards
                allowed]
            :param object_location: The storage location in which the search shall be executed [
                optional, defaults to ``GENESISArea.ALL``]
            :param result_count: The number of results that shall be returned
            :return: A parsed response containing the list of timeseries, if any were found
            """
            if variable_name is None:
                raise ValueError('The variable_name is a required parameter')
            if not (1 <= len(variable_name.strip()) <= 15):
                raise ValueError('The length of the variable name may not exceed 15 characters')
            if timeseries_selector and not (1 <= len(timeseries_selector.strip()) <= 15):
                raise ValueError("If a timeseries_selector is supplied its length may not exceed "
                                 "15 characters")
            # Build the query parameters
            _query_parameter = self._base_parameter | {
                'name': variable_name,
                'selection': '' if timeseries_selector is None else timeseries_selector,
                'area': object_location.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/timeseries2variable'
            return await tools.get_parsed_response(
                _url, _query_parameter, Catalogue.TimeseriesResponse
            )
        
        async def values(
                self,
                value_filter: str,
                object_location: GENESISArea = GENESISArea.ALL,
                search_by: GENESISValueCriteria = GENESISValueCriteria.CODE,
                sort_by: GENESISValueCriteria = GENESISValueCriteria.CODE,
                result_count: int = 100
        ) -> Catalogue.ValueResponse:
            """Get a list of values specified by the filter
            
            :param value_filter: The filter for the value identifications [optional, wildcards
                allowed]
            :param object_location: The storage location which shall be used during the search [
            optional, defaults to ``GENESISValueCriteria.CODE``]
            :param search_by: The criteria which is used in combination to the value_filter [
            optional, defaults to ``GENESISValueCriteria.CODE``]
            :param sort_by: The criteria by which the results are sorted [optional, defaults to
            ``GENESISValueCriteria.CODE``]
            :param result_count: The number of results returned
            :return: A parsed response containing the list of values
            """
            # Check the received variables
            if value_filter is None:
                raise ValueError('The value_filter is a required parameter')
            if not 1 <= len(value_filter.strip()) <= 15:
                raise ValueError('The length of the value_filter needs to be at least 1 character '
                                 'and may not exceed 15 characters')
            if not 1 <= result_count <= 2500:
                raise ValueError('The number of results returned needs to be greater than 1, '
                                 'but may not exceed 2500')
            # Build the query parameters
            params = self._base_parameter | {
                'selection': value_filter,
                'area': object_location.value,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'pagelength': result_count
            }
            _url = self._service_url + '/values'
            return await tools.get_parsed_response(
                _url, params, Catalogue.ValueResponse
            )
        
        async def values2variable(
                self,
                variable_name: str,
                value_filter: Optional[str] = None,
                object_location: GENESISArea = GENESISArea.ALL,
                search_by: GENESISVariableCriteria = GENESISVariableCriteria.CODE,
                sort_by: GENESISVariableCriteria = GENESISVariableCriteria.CODE,
                result_count: int = 100
        ) -> Catalogue.ValueResponse:
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
                raise ValueError('The variable_name is a required parameter and may not be empty')
            if not (1 <= len(variable_name.strip()) <= 15):
                raise ValueError('The length of the variable_name may not exceed 15 characters '
                                 'and may not be below 1 character')
            if '*' in variable_name:
                raise ValueError('The variable_name may not contain any wildcards (*)')
            # Check the value filter
            if value_filter and not (1 <= len(value_filter.strip()) <= 15):
                raise ValueError('The length of the value_filter may not exceed 15 characters and '
                                 'may not be below 1')
            # Check the number of results returned
            if not 1 <= result_count <= 2500:
                raise ValueError('The number of results returned needs to be greater than 1, '
                                 'but may not exceed 2500')
            # Create the query parameter
            _param = self._base_parameter | {
                'name': variable_name,
                'selection': value_filter,
                'area': object_location.value,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'pagelength': result_count
            }
            # Build the url for the call
            _url = self._service_url + '/values2variable'
            # Make the call and await the response
            return await tools.get_parsed_response(
                _url, _param, Catalogue.ValueResponse
            )

        async def variables(
                self,
                variable_filter: str,
                object_location: GENESISArea = GENESISArea.ALL,
                search_by: GENESISVariableCriteria = GENESISVariableCriteria.CODE,
                sort_by: GENESISVariableCriteria = GENESISVariableCriteria.CODE,
                variable_type: GENESISVariableType = GENESISVariableType.ALL,
                result_count: int = 100
        ) -> Catalogue.VariableResponse:
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
                raise ValueError('The variable_filter is a required parameter any may not be empty')
            if not (1 <= len(variable_filter.strip()) <= 6):
                raise ValueError('The variable_filter may only contain up to 6 characters')
            # Check if the result count is set properly
            if not (1 <= result_count <= 2500):
                raise ValueError('The number of possible results needs to be between 1 and 2500')
            # Build the query parameters
            _param = self._base_parameter | {
                'selection': variable_filter,
                'area': object_location.value,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'type': variable_type.value,
                'pagelength': result_count
            }
            # Build the url
            _url = self._service_url + '/variables'
            # Return the parsed result
            return await tools.get_parsed_response(
                _url, _param, Catalogue.VariableResponse
            )
            
            
