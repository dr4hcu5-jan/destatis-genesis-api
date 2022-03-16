"""A package containing the enums used in the main code"""
from enum import Enum, IntEnum


class GENESISLanguage(str, Enum):
    """The languages supported by the GENESIS API"""
    
    GERMAN = 'de'
    ENGLISH = 'en'


class GENESISCategory(str, Enum):
    """Categories which are available during the search"""
    
    TABLES = 'tables'
    STATISTICS = 'statistics'
    DATA_CUBES = 'cubes'
    VARIABLES = 'variables'
    TIME_SERIES = 'time_series'
    ALL = 'all'


class GENESISJobType(str, Enum):
    """
    The different types of jobs that are available on the GENESIS database
    """
    ALL = 'all'
    IMPORT = 'Import'
    EXPORT = 'Export'
    VALUE_RETRIEVAL = 'Werteabruf'
    CALCULATE_SUM_CUBES = 'Summenquader berechnen'
    CLEANUP_DATA_CUBES = 'Datenquader bereinigen'


class GENESISJobCriteria(str, Enum):
    """
    Criteria for searching and sorting jobs
    """
    
    CODE = 'Code'
    STATUS = 'Status'
    TYPE = 'Auftragstyp'
    TIME = 'Zeitpunkt'


class GENESISObjectType(str, Enum):
    """
    Types of objects that are available in the database
    """
    ALL = 'Alle'
    TABLE = 'Tabellen'
    STATISTIC = 'Statistiken'
    STATISTIC_UPDATE = 'StatistikUpdates'


class GENESISStatisticCriteria(str, Enum):
    """
    Criteria for searching and sorting jobs
    """
    
    CODE = 'Code'
    CONTENT = 'Inhalt'


class GENESISArea(str, Enum):
    """
    Locations of objects
    """
    
    USER = 'Benutzer'
    GROUP = 'Gruppe'
    OFFICE = 'Amt'
    PUBLIC = 'Öffentlich'
    ALL = 'Alle'


class GENESISTableCriteria(str, Enum):
    """
    Criteria for searching and sorting jobs
    """
    
    CODE = 'Code'
    TOP = 'Top'


class GENESISValueCriteria(str, Enum):
    CODE = 'Code'
    CONTENT = 'Inhalt'


class GENESISVariableCriteria(str, Enum):
    CODE = 'Code'
    CONTENT = 'Inhalt'


class GENESISVariableType(str, Enum):
    ALL = 'Alle'
    CLASSIFYING = 'klassifizierend'
    TOTAL = 'insgesamt'
    SPATIAL = 'räumlich'
    FACTUAL = 'sachlich'
    VALUE = 'wert'
    TEMPORAL = 'zeitlich'
    TIME_IDENTIFYING = 'zeitidentifizierend'


class GENESISChartType(IntEnum):
    """The different chart types supported by the database"""
    
    LINE_CHART = 0
    BAR_CHART = 1
    PIE_CHART = 2
    POINT_CLOUD = 3


class GENESISImageSize(IntEnum):
    """The different image size levels"""
    
    LEVEL_0 = 0
    """Image resolution of: 480x320 pixels"""
    
    LEVEL_1 = 1
    """Image resolution of: 640x480 pixels"""
    
    LEVEL_2 = 2
    """Image resolution of: 800x600 pixels"""
    
    LEVEL_3 = 3
    """Image resolution of: 1024x768 pixels (recommended size)"""
