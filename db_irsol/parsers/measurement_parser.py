# Internal dependencies
from db_irsol.third_party import z3readbd
from db_irsol.parsers.utility import get_file_md5
from db_irsol.parsers.utility import filter_string_parameters
from db_irsol.settings import Settings

# libraries dependencies
from astropy.io import fits
import re
import os


class MeasurementParser:
    WLENGTH_FILE_NAME_PATTERN = '[0-9]{4}(\.[0-9]{2})?'

    @staticmethod
    def parse_z3db_file(measurement_file_path):
        parameters = {'measurement_file_hash': get_file_md5(measurement_file_path)}

        header = {}
        z3readbd.z3readbd(measurement_file_path, header, get_header=True)

        for key, value in Settings.FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES.items():
            if key in header:
                print(header[key])
                parameters[value] = header[key]

        # The following line of code are to further process the data extracted.
        return MeasurementParser. \
            __post_parse_measurement_parameters(measurement_file_path, parameters,
                                                Settings.FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES)

    @staticmethod
    def parse_fits_file(measurement_file_path):
        parameters = {'measurement_file_hash': get_file_md5(measurement_file_path)}

        file_fits = fits.open(measurement_file_path)
        header = file_fits[0].header

        for key, value in Settings.FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES.items():
            if key in header:
                parameters[value] = header[key]

        # The following line of code are to further process the data extracted.
        return MeasurementParser. \
            __post_parse_measurement_parameters(measurement_file_path, parameters,
                                                Settings.FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES)

    @staticmethod
    def __post_parse_measurement_parameters(measurement_file_path, parameters, fields_to_columns):

        # Date formatting

        if 'DATE' in fields_to_columns and fields_to_columns['DATE'] in parameters:
            parameters[fields_to_columns['DATE']] = re.sub("\\+.*", "",
                                                           parameters[fields_to_columns['DATE']].replace("T", " "))

        if 'DATE_END' in fields_to_columns and fields_to_columns['DATE_END'] in parameters:
            parameters[fields_to_columns['DATE_END']] = re.sub("\\+.*", "",
                                                               parameters[fields_to_columns['DATE_END']].replace("T",
                                                                                                                 " "))
        if fields_to_columns['WLENGTH'] not in parameters:
            measurement_file_name = os.path.basename(os.path.normpath(measurement_file_path))
            match = re.search(MeasurementParser.WLENGTH_FILE_NAME_PATTERN, measurement_file_name, re.IGNORECASE)
            if match is not None:
                parameters[fields_to_columns['WLENGTH']] = match.group(0)

        parameters = filter_string_parameters(parameters)

        return parameters
