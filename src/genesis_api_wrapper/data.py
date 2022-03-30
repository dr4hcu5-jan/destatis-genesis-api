import datetime
import typing

from . import enums, tools


class DataAPIWrapper:
    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new part wrapper for the methods listed in the DataAPIWrapper (2.5) section

        :param username: The username which is used to access the database
        :param password: The password which is used to access the database
        :param language: The language used in responses by the database
        """
        # Check that the username is not None
        if not username:
            raise ValueError(
                "There was no username supplied during the creation of the " "section wrapper"
            )
        if not len(username) == 10:
            raise ValueError("The username has not the required length of 10 characters")
        # Check that a password is supplied
        if not password:
            raise ValueError(
                "There was no password supplied during the creation of the " "section wrapper"
            )
        # Check that the password is between 10 and 20 characters long
        if not 10 <= len(password) <= 20:
            raise ValueError(
                "The password has not the required length of at least 10 "
                "characters and 20 characters"
            )
        # Save the service path
        self._service_path = "/data"
        # Create the base parameters
        self._base_parameter = {
            "username": username,
            "password": password,
            "language": language.value,
        }

    async def chart2result(
        self,
        # Selection Specifiers
        object_name: str,
        # Chart Settings
        chart_type: enums.ChartType.LINE_CHART,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
        draw_points_in_line_chart: bool = False,
        compress_y_axis: bool = False,
        show_top_values_first: bool = False,
        # Object Storage Settings
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
    ) -> dict:
        """Download a graph for a result table

        The file will be downloaded into a local temporary path. The path to the image will be
        returned instead of the whole image

        :param object_location: The location in which the object is stored, defaults
            to :py:enum:mem:`~enums.GENESISArea`
        :type object_location: enums.ObjectStorage
        :param object_name: The identifier of the result table [required]
        :type object_name: str
        :param chart_type: The type of chart which shall be downloaded [required]
        :type chart_type: enums.ChartType
        :param image_size: The size of the image which shall be downloaded [optional,
            default 1024x768 pixels]
        :type image_size: enums.ImageSize
        :param draw_points_in_line_chart: Highlight data points in a line chart [optional,
            only allowed if chart_type is line chart]
        :type draw_points_in_line_chart: bool
        :param compress_y_axis: Compress the y-axis to fit the values
        :type compress_y_axis: bool
        :param show_top_values_first:
            When using a Pie Chart:
                Display the top five (5) values and group all other values into one extra slice
            When using any other type of chart:
                Show the top four (4) values from the dataset instead of the first four values
        :type show_top_values_first: bool
        :return: The path to the image or the response from the server if there is an error
        :rtype: dict
        """
        # Check if the object name is set correctly
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        # Check if the length of the object name is between 1 and 15 characters
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Validate that a chart type is set:
        if chart_type is None:
            raise ValueError("The chart_type is a required parameter")
        # Check that draw_points_in_line_chart is only working if the chart type is line chart
        if draw_points_in_line_chart and chart_type != enums.ChartType.LINE_CHART:
            raise ValueError(
                "The parameter draw_points_in_line_chart is only supported for "
                "enums.ChartType.LINE_CHART"
            )
        # Build the query parameters
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "enums.ChartType": chart_type.value,
            "drawpoints": str(draw_points_in_line_chart),
            "zoom": image_size.value,
            "focus": str(compress_y_axis),
            "tops": str(show_top_values_first),
            "format": "png",
        }
        # Build the query path
        query_path = self._service_path + "/chart2result"
        # Download the image
        return await tools.get_database_response(query_path, query_parameter)

    async def chart2table(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Chart settings:
        chart_type: enums.ChartType = enums.ChartType.LINE_CHART,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
        draw_points_in_line_chart: bool = False,
        compress_y_axis: bool = False,
        show_top_values_first: bool = False,
        time_slices: int = None,
    ) -> dict:
        """Download a graph for a table

        The image of the graph will be downloaded into a temporary directory and the path to
        the image will be returned

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param chart_type: The type of chart which shall be downloaded, defaults to
            :attr:`~enums.ChartType.LINE_CHART`
        :type chart_type: enums.ChartType, optional
        :param image_size: The size of the image which shall be downloaded, defaults to
            :attr:`~enums.ImageSize.LEVEL3`
        :type image_size: enums.ImageSize, optional
        :param draw_points_in_line_chart: Highlight the data points in a line chart,
            only allowed if chart_type is :attr:`enums.ChartType.LINE_CHART`
        :type draw_points_in_line_chart: bool, optional
        :param compress_y_axis: Compress the y-axis to fit the values
        :type compress_y_axis: bool, optional
        :param show_top_values_first:
            When using :attr:`enums.ChartType.PIE_CHART` as chart_type:
                Display the top five (5) values as single slices and group all other slices into
                one other slice.
            When using any other :class:`enums.ChartType`:
                Display the top four (4) values instead of the first four (4) values
        :type show_top_values_first: bool, optional
        :param time_slices: The number of time slices into which the data shall be accumulated
        :type time_slices: int, optional
        :return: The path to the image or the file downloaded from the server.
        :rtype: dict
        """
        # Check if the table name was set correctly
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Check if any illegal parameter combination was set
        if draw_points_in_line_chart and chart_type is not enums.ChartType.LINE_CHART:
            raise ValueError(
                "The parameter draw_points_in_line_chart is only supported for "
                "enums.ChartType.LINE_CHART"
            )
        # Convert the times to string
        _time_string = (
            None if updated_after is None else updated_after.strftime("%d.%m.%Y %H:%M:%Sh")
        )
        # Build the query parameters
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "enums.ChartType": chart_type.value,
            "drawpoints": str(draw_points_in_line_chart),
            "zoom": image_size.value,
            "focus": str(compress_y_axis),
            "tops": str(show_top_values_first),
            "startyear": start_year,
            "endyear": end_year,
            "timeslices": time_slices,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "png",
            "stand": _time_string,
        }
        # Build the query path
        query_path = self._service_path + "/chart2table"
        # Download the image
        return await tools.get_database_response(query_path, query_parameter)

    async def chart2timeseries(
        self,
        object_name: str,
        # Selection Specifier
        contents: typing.Optional[list[str]] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Chart settings:
        chart_type: enums.ChartType = enums.ChartType.LINE_CHART,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
        draw_points_in_line_chart: bool = False,
        compress_y_axis: bool = False,
        show_top_values_first: bool = False,
        time_slices: int = None,
    ) -> dict:
        """Download a graph for a timeseries

        The image of the graph will be downloaded into a temporary directory and the path to
        the image will be returned

        :param object_name: The identifier of the timeseries
        :type object_name: str
        :param contents: The names of the values which shall be in the chart
        :type contents: list[str], optional
        :param object_location: The location in which the table is stored,
            defaults to :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: enums.ObjectStorage, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param chart_type: The type of chart which shall be downloaded, defaults to
            :py:enum:mem:`~enums.ChartType.LINE_CHART`
        :type chart_type: enums.ChartType, optional
        :param image_size: The size of the image which shall be downloaded, defaults to
            :py:enum:mem:`~enums.ImageSize.LEVEL_3`
        :type image_size: enums.ImageSize, optional
        :param draw_points_in_line_chart: Highlight the data points in a line chart,
            only allowed if chart_type is :attr:`enums.ChartType.LINE_CHART`
        :type draw_points_in_line_chart: bool, optional
        :param compress_y_axis: Compress the y-axis to fit the values
        :type compress_y_axis: bool, optional
        :param show_top_values_first:
            When using :py:enum:mem:`~enums.ChartType.PIE_CHART` as chart_type:
                Display the top five (5) values as single slices and group all other slices into
                one other slice.
            When using any other :enum:`~enums.ChartType`:
                Display the top four (4) values instead of the first four (4) values
        :type show_top_values_first: bool, optional
        :param time_slices: The number of time slices into which the data shall be accumulated
        :type time_slices: int, optional
        :return: The path to the image or the file downloaded from the server.
        :rtype: dict
        """
        # Check if the table name was set correctly
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Check if any illegal parameter combination was set
        if draw_points_in_line_chart and chart_type is not enums.ChartType.LINE_CHART:
            raise ValueError(
                "The parameter draw_points_in_line_chart is only supported for "
                "enums.ChartType.LINE_CHART"
            )
        # Convert the times to string
        _time_string = (
            None if updated_after is None else updated_after.strftime("%d.%m.%Y %H:%M:%Sh")
        )
        # Build the query parameters
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "enums.ChartType": chart_type.value,
            "drawpoints": str(draw_points_in_line_chart),
            "zoom": image_size.value,
            "focus": str(compress_y_axis),
            "tops": str(show_top_values_first),
            "contents": ",".join(contents) if contents is not None else None,
            "startyear": start_year,
            "endyear": end_year,
            "timeslices": time_slices,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "png",
            "stand": _time_string,
        }
        # Build the query path
        query_path = self._service_path + "/chart2timeseries"
        # Download the image
        return await tools.get_database_response(query_path, query_parameter)

    async def cube(
        self,
        object_name: str,
        # Selection Specifier
        contents: typing.Optional[list[str]] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Cube settings
        values: bool = True,
        metadata: bool = True,
        additional_metadata: bool = False,
        time_slices: int = None,
    ) -> dict:
        """Get a datacube embedded into an dictionary

        This method requires the "premium" access to the database.

        :param object_name: The identifier of the data cube
        :type object_name: str
        :param contents: The names of the values which shall be in the chart
        :type contents: list[str], optional
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.GENESISObjectLocation.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param values: Should values be returned, defaults to `True`
        :type values: bool, optional
        :param metadata: Should metadata be returned, defaults to `True`
        :type metadata: bool, optional
        :param additional_metadata: Should additional metadata be returned, defaults to `False`
        :type additional_metadata: bool, optional
        :param time_slices: The number of time slices into which the data shall be accumulated
        :type time_slices: int, optional
        :return: The csv embedded in the response body
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Convert the times to string
        _time_string = (
            None if updated_after is None else updated_after.strftime("%d.%m.%Y %H:%M:%Sh")
        )
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "contents": ",".join(contents) if contents is not None else None,
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "csv",
            "stand": _time_string,
            "values": str(values),
            "metadata": str(metadata),
            "additionals": str(additional_metadata),
        }
        # Build the query path
        query_path = self._service_path + "/cube"
        # Download the file
        return await tools.get_database_response(query_path, query_parameters)

    async def cube_file(
        self,
        object_name: str,
        # Selection Specifier
        contents: typing.Optional[list[str]] = None,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Cube settings
        values: bool = True,
        metadata: bool = True,
        additional_metadata: bool = False,
        time_slices: int = None,
    ):
        """Download a data cube as csv-file (seperator: `;`)

        This method requires the "premium" access to the database.

        :param object_name: The identifier of the data cube
        :type object_name: str
        :param contents: The names of the values which shall be in the chart
        :type contents: list[str], optional
        :param object_location: The location in which the table is stored,
            defaults to :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: enums.ObjectStorage, optional
        :param updated_after: Time after which the table needs to have been
            updated to be returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the
            chart, defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart,
            defaults to :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used
            to limit the regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used
            to limit the data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be
            used to limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used
            to limit the data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be
            used to limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used
            to limit the data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be
            used to limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param values: Should values be returned, defaults to `True`
        :type values: bool, optional
        :param metadata: Should metadata be returned, defaults to `True`
        :type metadata: bool, optional
        :param additional_metadata: Should additional metadata be returned,
            defaults to `False`
        :type additional_metadata: bool, optional
        :param time_slices: The number of time slices into which the data shall
            be accumulated
        :type time_slices: int, optional
        :return: The csv embedded in the response body
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Convert the times to string
        _time_string = (
            None if updated_after is None else updated_after.strftime("%d.%m.%Y %H:%M:%Sh")
        )
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "contents": ",".join(contents) if contents is not None else None,
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "csv",
            "stand": _time_string,
            "values": str(values),
            "metadata": str(metadata),
            "additionals": str(additional_metadata),
        }
        # Build the query path
        query_path = self._service_path + "/cubefile"
        # Download the file
        return await tools.get_database_response(query_path, query_parameters)

    async def map2result(
        self,
        object_name: str,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        number_of_distinction_classes: typing.Optional[int] = 5,
        classify_by_same_value_range: typing.Optional[bool] = True,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
    ):
        """Download a map displaying the values of the specified result table

        :param object_name: The identifier of the data cube
        :type object_name: str
        :param object_location: The location in which the table is stored,
            defaults to :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: enums.ObjectStorage, optional
        :param number_of_distinction_classes: The number of distinction classes to be
            generated, defaults to 5
        :type number_of_distinction_classes: int, optional
        :param classify_by_same_value_range: If this is set to `True`, the distinction classes
            have the same size. If this is set to `False` the distinction classes have
            different sizes, but the same amount of values in them. Defaults to `True`
        :type classify_by_same_value_range: bool, optional
        :param image_size: The size of the image which shall be downloaded, defaults to
            :py:enum:mem:`~enums.ImageSize.LEVEL_3`
        :type image_size: enums.ImageSize, optional
        :return: The path to the image or the file downloaded from the server.
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        if not (2 <= number_of_distinction_classes <= 5):
            raise ValueError("The number of distinction classes need to be between 2 and 5")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "mapType": 0,
            "classes": number_of_distinction_classes,
            "classification": int(classify_by_same_value_range),
            "zoom": image_size.value,
            "format": "png",
        }
        # Build the query path
        query_path = self._service_path + "/map2result"
        # Download the file
        return await tools.get_database_response(query_path, query_parameters)

    async def map2table(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Map Settings
        number_of_distinction_classes: typing.Optional[int] = 5,
        classify_by_same_value_range: typing.Optional[bool] = True,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
    ):
        """
        Download a map visualizing the selected data from the table

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param number_of_distinction_classes: The number of distinction classes to be
            generated, defaults to 5
        :type number_of_distinction_classes: int, optional
        :param classify_by_same_value_range: If this is set to `True`, the distinction classes
            have the same size. If this is set to `False` the distinction classes have
            different sizes, but the same amount of values in them. Defaults to `True`
        :type classify_by_same_value_range: bool, optional
        :param image_size: The size of the image which shall be downloaded, defaults to
            :py:enum:mem:`~enums.ImageSize.LEVEL_3`
        :type image_size: enums.ImageSize, optional
        :return: The path to the image or the file downloaded from the server.
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        if not (2 <= number_of_distinction_classes <= 5):
            raise ValueError("The number of distinction classes need to be between 2 and 5")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "mapType": 0,
            "classes": number_of_distinction_classes,
            "classification": int(classify_by_same_value_range),
            "zoom": image_size.value,
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "png",
        }
        # Build the query path
        query_path = self._service_path + "/map2table"
        # Download the file
        return await tools.get_database_response(query_path, query_parameters)

    async def map2timeseries(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Map Settings
        number_of_distinction_classes: typing.Optional[int] = 5,
        classify_by_same_value_range: typing.Optional[bool] = True,
        image_size: enums.ImageSize = enums.ImageSize.LEVEL_3,
    ):
        """
        Download a map visualizing the selected data from the table

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: Data starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: Data after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param number_of_distinction_classes: The number of distinction classes to be
            generated, defaults to 5
        :type number_of_distinction_classes: int, optional
        :param classify_by_same_value_range: If this is set to `True`, the distinction classes
            have the same size. If this is set to `False` the distinction classes have
            different sizes, but the same amount of values in them. Defaults to `True`
        :type classify_by_same_value_range: bool, optional
        :param image_size: The size of the image which shall be downloaded, defaults to
            :py:enum:mem:`~enums.ImageSize.LEVEL_3`
        :type image_size: enums.ImageSize, optional
        :return: The path to the image or the file downloaded from the server.
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        if not (2 <= number_of_distinction_classes <= 5):
            raise ValueError("The number of distinction classes need to be between 2 and 5")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "mapType": 0,
            "classes": number_of_distinction_classes,
            "classification": int(classify_by_same_value_range),
            "zoom": image_size.value,
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "format": "png",
        }
        # Build the query path
        query_path = self._service_path + "/map2timeseries"
        # Download the file
        return await tools.get_database_response(query_path, query_parameters)

    async def result(
        self,
        object_name: str,
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        remove_empty_rows: bool = False,
    ):
        """
        Get the contents of the result table embedded in the response

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param remove_empty_rows: Remove empty rows from the embedded CSV-file
        :type remove_empty_rows: bool, optional
        :return: Dictionary containing the response
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build query parameters
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "compress": str(remove_empty_rows),
        }
        query_path = self._service_path + "/result"
        return await tools.get_database_response(query_path, query_parameter)

    async def table(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Output Selection
        generate_job: bool = False,
        remove_emtpy_rows: bool = False,
        switch_rows_and_columns: bool = False,
    ):
        """
        Download a table by embedding it into the JSON Response

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param generate_job: Generate a Job if the table cannot be pulled directly, defaults
            to ``False``
        :type generate_job: bool
        :param remove_emtpy_rows: Remove all empty data rows from the response, defaults to
            ``False``
        :type remove_emtpy_rows: bool
        :param switch_rows_and_columns: Switch the rows and columns in the response,
            defaults to ``False``
        :type switch_rows_and_columns: bool
        :return: The specified table data embedded in the response data
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "compress": str(remove_emtpy_rows),
            "transpose": str(switch_rows_and_columns),
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "job": str(generate_job),
        }
        # Build the query path
        query_path = self._service_path + "/table"
        # Get the response
        return await tools.get_database_response(query_path, query_parameters)

    async def tablefile(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Output Selection
        generate_job: bool = False,
        remove_emtpy_rows: bool = False,
        switch_rows_and_columns: bool = False,
        file_format: enums.FileFormat = enums.FileFormat.CSV,
    ):
        """
        Download a table as file

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param generate_job: Generate a Job if the table cannot be pulled directly, defaults
            to ``False``
        :type generate_job: bool
        :param remove_emtpy_rows: Remove all empty data rows from the response, defaults to
            ``False``
        :type remove_emtpy_rows: bool
        :param switch_rows_and_columns: Switch the rows and columns in the response,
            defaults to ``False``
        :type switch_rows_and_columns: bool
        :param file_format: The file format which shall be returned, defaults to
            :py:enum:mem:`~enums.FileType.CSV`
        :type file_format: enums.FileType
        :return: The specified table data embedded in the response data
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "compress": str(remove_emtpy_rows),
            "transpose": str(switch_rows_and_columns),
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "job": str(generate_job),
            "format": file_format.value,
        }
        # Build the query path
        query_path = self._service_path + "/tablefile"
        # Get the response
        return await tools.get_database_response(query_path, query_parameters)

    async def timeseries(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Output Selection
        generate_job: bool = False,
        remove_emtpy_rows: bool = False,
        switch_rows_and_columns: bool = False,
    ):
        """
        Download a timeseries embedded into a JSON response

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param generate_job: Generate a Job if the table cannot be pulled directly, defaults
            to ``False``
        :type generate_job: bool
        :param remove_emtpy_rows: Remove all empty data rows from the response, defaults to
            ``False``
        :type remove_emtpy_rows: bool
        :param switch_rows_and_columns: Switch the rows and columns in the response,
            defaults to ``False``
        :type switch_rows_and_columns: bool
        :return: The specified table data embedded in the response data
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "compress": str(remove_emtpy_rows),
            "transpose": str(switch_rows_and_columns),
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "job": str(generate_job),
        }
        # Build the query path
        query_path = self._service_path + "/timeseries"
        # Get the response
        return await tools.get_database_response(query_path, query_parameters)

    async def timeseriesfile(
        self,
        object_name: str,
        # Selection Specifier
        object_location: enums.ObjectStorage = enums.ObjectStorage.ALL,
        updated_after: typing.Optional[datetime.datetime] = None,
        start_year: typing.Optional[str] = None,
        end_year: typing.Optional[str] = None,
        region_code: typing.Optional[str] = None,
        region_key: typing.Optional[str] = None,
        # DataAPIWrapper Classifiers
        classifying_code_1: typing.Optional[str] = None,
        classifying_key_1: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_2: typing.Optional[str] = None,
        classifying_key_2: typing.Optional[typing.Union[str, list[str]]] = None,
        classifying_code_3: typing.Optional[str] = None,
        classifying_key_3: typing.Optional[typing.Union[str, list[str]]] = None,
        # Output Selection
        generate_job: bool = False,
        remove_emtpy_rows: bool = False,
        switch_rows_and_columns: bool = False,
    ):
        """
        Download a timeseries embedded into a JSON response

        :param object_name: The identifier of the table [required, 1-15 characters]
        :type object_name: str
        :param object_location: The location in which the table is stored, defaults to
            :py:enum:mem:`~enums.ObjectStorage.ALL`
        :type object_location: str, optional
        :param updated_after: Time after which the table needs to have been updated to be
            returned, defaults to :attr:`None`
        :type updated_after: datetime, optional
        :param start_year: DataAPIWrapper starting from this year will be selected for the chart ,
            defaults to :attr:`None`
        :type start_year: str, optional
        :param end_year: DataAPIWrapper after this year will be excluded for the chart, defaults to
            :attr:`None`
        :type end_year: str, optional
        :param region_code: Code of the regional classifier which shall be used to limit the
            regional component of the data, defaults to :attr:`None`
        :type region_code: str, optional
        :param region_key: The official municipality key (AGS) specifying from which
            municipalities the data shall be taken from, defaults to :attr:`None`
        :type region_key: str, optional
        :param classifying_code_1: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_1: str, optional
        :param classifying_key_1: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_1: str, optional
        :param classifying_code_2: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_2: str, optional
        :param classifying_key_2: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_2: str, optional
        :param classifying_code_3: Code of the classificator which shall be used to limit the
            data selection further, defaults to :attr:`None`
        :type classifying_code_3: str, optional
        :param classifying_key_3: Code of the classificator value which shall be used to
            limit the data selection further, defaults to :attr:`None`
        :type classifying_key_3: str, optional
        :param generate_job: Generate a Job if the table cannot be pulled directly, defaults
            to ``False``
        :type generate_job: bool
        :param remove_emtpy_rows: Remove all empty data rows from the response, defaults to
            ``False``
        :type remove_emtpy_rows: bool
        :param switch_rows_and_columns: Switch the rows and columns in the response,
            defaults to ``False``
        :type switch_rows_and_columns: bool
        :return: The specified table data embedded in the response data
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameters
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": object_location.value,
            "compress": str(remove_emtpy_rows),
            "transpose": str(switch_rows_and_columns),
            "startyear": start_year,
            "endyear": end_year,
            "regionalvariable": region_code,
            "regionalkey": region_key,
            "classifyingvariable1": classifying_code_1,
            "classifyingkey1": classifying_key_1,
            "classifyingvariable2": classifying_code_2,
            "classifyingkey2": classifying_key_2,
            "classifyingvariable3": classifying_code_3,
            "classifyingkey3": classifying_key_3,
            "job": str(generate_job),
            "format": "csv",
        }
        # Build the query path
        query_path = self._service_path + "/timeseriesfile"
        # Get the response
        return await tools.get_database_response(query_path, query_parameters)
