"""Responses which are received from the GENESIS database"""
from typing import Optional

from models import *
from .internals import *
from pydantic import validator


class BaseResponse(BaseModel):
    """
    A Basic Response which contains data that is always sent for every request
    """
    
    service_identification: ServiceIdent = Field(
        default=...,
        alias='Ident'
    )
    """Information about the called service"""

    request_status: Status = Field(
        default=...,
        alias='Status'
    )
    """Status information about the request"""

    request_parameter: RequestParameter = Field(
        default=...,
        alias='Parameter'
    )
    """The request parameter which where sent to the server"""
    
    copyright_notice: str = Field(
        default=...,
        alias='Copyright'
    )
    """A copyright notice indicating license information and who holds the copyright for the
    requested data"""


class HelloWorld:
    class WhoAmIResponse(BaseModel):
        """
        The contents of the response after requesting the "whoami" method on the api
        """
        
        user_agent: str = Field(
            default=...,
            alias='User-Agent',
            description='The user-agent header present in the request which was send'
        )
        
        user_ip: str = Field(
            default=...,
            alias='User-IP',
            description='The IP address from which the call was made'
        )
    
    class LoginCheckResponse(BaseModel):
        """The contents of the response after requesting the "logincheck" method on the api"""
        
        username: str = Field(
            default=...,
            alias='Username'
        )
        
        status: str = Field(
            default=...,
            alias='Status'
        )


class Find:
    """Responses for requests in the /find resources"""

    class FindResult(BaseResponse):
        """The contents of a find request"""
        
        data_cubes: Optional[list[CubeInformation]] = Field(
            default=None,
            alias='Cubes'
        )
        """A list of data cubes which matched the find request"""
        
        statistics: Optional[list[StatisticInformation]] = Field(
            default=None,
            alias='Statistics'
        )
        "A list of statistics which matched with the find request"
        
        tables: Optional[list[TableInformation]] = Field(
            default=None,
            alias='Tables'
        )
        """A list of tables which matched with the find request"""
        
        time_series: Optional[list[TimeSeriesInformation]] = Field(
            default=None,
            alias='Timeseries'
        )
        """A list of time series which matched with the find request"""
        
        variables: Optional[list[VariableInformation]] = Field(
            default=...,
            alias='Variables'
        )
        """A list of variables which matched with the find request"""


class Catalogue:
    """Responses for requests in the /catalogue resources"""
    
    class CubeResponse(BaseResponse):
        """A response for requesting lists for cubes"""
        
        cube_list: Optional[list[CubeInformation]] = Field(
            default=None,
            alias='List'
        )
        
    class JobResponse(BaseResponse):
        """A response for getting a list of Jobs (e.g. getting big tables)"""
        
        job_list: Optional[list[JobInformation]] = Field(
            default=None,
            alias='List'
        )
        
    class ModifiedDataResponse(BaseResponse):
        """A response for getting a list of changes made to the database entries"""
        
        changed_objects: Optional[list[Optional[ModifiedDataInformation]]] = Field(
            default=None,
            alias='List'
        )
        
        @validator('changed_objects', pre=True)
        def remove_none_values_from_list(cls, value: list) -> list[ModifiedDataInformation]:
            """Removed the None entries from the list
            
            :param value: The list of data
            :return:
            """
            return [v for v in value if v]
    
    class QualitySignsResponse(BaseResponse):
        """
        A response containing the currently active quality signs
        """
        
        quality_signs: Optional[list[QualitySignInformation]] = Field(
            default=None,
            alias='List'
        )
    
    class ResultTableResponse(BaseResponse):
        """
        A response containing information about the requested result tables
        """
        
        result_tables: Optional[list[ResultTableInformation]] = Field(
            default=...,
            alias='List'
        )
