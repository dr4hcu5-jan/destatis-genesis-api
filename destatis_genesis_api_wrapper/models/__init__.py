from datetime import datetime, date, time
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel, root_validator
from pydantic import Field, constr, validator, Extra


class BaseModel(PydanticBaseModel):
    """
    A Basic Class used for all responses from the GENESIS database which presets some
    configuration variables
    """
    
    class Config:
        """Configuration which is inherited into every other Response"""
        
        allow_population_by_field_name = True
        """Allow the population of the fields by their names and aliases"""


class ObjectInformation(BaseModel):
    """
    Information about a generic Object found in the GENESIS database
    """
    
    identification: constr(min_length=1) = Field(
        default=...,
        alias='Code',
    )
    """
    Identification Code
    
    The identification code used by the GENESIS database to identify a resource or object
    """
    
    description: Optional[str] = Field(
        default=None,
        alias='Content',
    )
    """
    Content Description
    
    A textual description of the contents of the object. This may not be set or be an emtpy
    string depending on the object or resource
    """


class CubeInformation(ObjectInformation):
    """
    Information about a data cube
    """
    
    state: str = Field(
        default=...,
        alias='State'
    )
    """
    State of the data cube
    
    This string indicates the state of the content of the data cube
    """
    
    time_span: str = Field(
        default=...,
        alias='Time'
    )
    """
    Time span
    
    A textual description about the time span which is included in the data cube
    """
    
    last_update: int = Field(
        default=...,
        alias='LatestUpdate'
    )
    """
    Last Update
    
    A UNIX timestamp indicating the point of time at which this has been updated the last time
    """
    
    extra_information: bool = Field(
        default=...,
        alias='Information'
    )
    """
    Extra Information
    
    Boolean indicator if this data cube has extra information present
    """
    
    @validator('last_update', pre=True, allow_reuse=True)
    def convert_string_to_unix_timestamp(cls, v):
        """Convert the input string into a UNIX timestamp
        
        :param v: The string which shall be converted
        :return:
        """
        input_format = '%d.%m.%Y %H:%M:%Sh'
        _datetime = datetime.strptime(v, input_format)
        return _datetime.timestamp()


class StatisticInformation(ObjectInformation):
    """
    Information about a statistic found in the GENESIS database
    """
    
    cubes: int = Field(
        default=...,
        alias='Cubes'
    )
    """
    Number of cubes
    
    The number of cubes which are assigned to the Statistic
    """
    
    extra_information: bool = Field(
        default=...,
        alias='Information'
    )
    """
    Extra Information

    Boolean indicator if this data cube has extra information present
    """


class TableInformation(ObjectInformation):
    """
    Information about a table found in the GENESIS database
    """
    
    time: str = Field(
        default=...,
        alias='Time'
    )
    """
    Time span
    
    Information about the time period displayed in the table
    """


class TimeSeriesInformation(ObjectInformation):
    """
    Information about a time series found in the GENESIS database"""
    
    state: str = Field(
        default=...,
        alias='State'
    )
    """The state of the timeseries"""
    
    time_range: str = Field(
        default=...,
        alias='Time'
    )
    """The time range available in the time series"""
    
    last_update: datetime = Field(
        default=...,
        alias='LatestUpdate'
    )
    """Time of the last update of the timeseries"""
    
    extra_information: bool = Field(
        default=...,
        alias='Information'
    )
    """
    Extra Information

    Boolean indicator if this data cube has extra information present
    """
    
    @validator('last_update', pre=True, allow_reuse=True)
    def convert_string_to_unix_timestamp(cls, v):
        """Convert the input string into a UNIX timestamp

        :param v: The string which shall be converted
        :return:
        """
        input_format = '%d.%m.%Y %H:%M:%Sh'
        _datetime = datetime.strptime(v, input_format)
        return _datetime.timestamp()


class VariableInformation(ObjectInformation):
    """
    Information about a variable found in the GENESIS database
    """
    
    type: str = Field(
        default=...,
        alias='Type'
    )
    """
    Type of variable
    
    Textual information about the type of the variable
    """
    
    values: int = Field(
        default=...,
        alias='Values'
    )
    """
    Number of values
    
    Number of values associated to the variable
    """
    
    extra_information: bool = Field(
        default=...,
        alias='Information'
    )
    """
    Extra Information

    Boolean indicator if this data cube has extra information present
    """


class JobInformation(ObjectInformation):
    """
    Information about a Job present in the GENESIS database
    """
    
    job_date: date = Field(
        default=...,
        alias='Date'
    )
    """
    Date Information
    
    Due to missing documentation for the GENESIS API no further information is present at the moment
    """
    
    job_time: time = Field(
        default=...,
        alias='Time'
    )
    """
    Time Information
    
    Due to missing documentation for the GENESIS API no further information is present at the moment
    """
    
    state: str = Field(
        default=...,
        alias='State'
    )
    """
    Job State Information
    
    The state of the job
    """
    
    @validator('job_date', pre=True, allow_reuse=True)
    def convert_date_string_to_date(cls, v) -> date:
        """Convert the date to a datetime object
        
        :param v: The date string
        :return: A date object
        """
        day, month, year = v.split('.')
        return date(year, month, day)
    
    @validator('job_time', pre=True, allow_reuse=True)
    def convert_time_string_to_time(cls, v) -> time:
        """Convert the time string to a time object
        
        :param v: The time string
        :return: A time object
        """
        hour, minute, second = v.split(':')
        return time(hour, minute, second)


class ModifiedDataInformation(ObjectInformation):
    """Information about a modified dataset"""
    
    type: str = Field(
        default=...,
        alias='Type'
    )
    """The type of dataset that has been modified"""
    
    change_date: date = Field(
        default=...,
        alias='Date'
    )
    """The date of the change"""
    
    added: str = Field(
        default=...,
        alias='Added'
    )
    """Information about what has been added"""
    
    @validator('change_date', pre=True, allow_reuse=True)
    def convert_date_string_to_date(cls, v) -> date:
        """Convert the date to a datetime object

        :param v: The date string
        :return: A date object
        """
        day, month, year = v.split('.')
        return date(int(year), int(month), int(day))


class QualitySignInformation(ObjectInformation):
    """Information about a quality sign"""
    pass


class ResultTableInformation(ObjectInformation):
    """Information about a result table"""
    
    values: int = Field(
        default=...,
        alias='Values'
    )
    """Number of values associated with the table"""


class TermInformation(BaseModel):
    term: str = Field(
        default=...,
        alias='Content'
    )
    """The content of the term"""
