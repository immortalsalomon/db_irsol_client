# External package dependencies
from db_irsol.third_party import z3readbd

# Internal package dependencies
from utility import get_file_md5
import constants

# libraries dependencies
from astropy.io import fits
import re


class MeasurementParser:

    @staticmethod
    def parse_z3db_file(measurement_file_path):
        parameters = {'measurement_file_hash': get_file_md5(measurement_file_path)}

        header = z3readbd.z3readbd(measurement_file_path, get_header=True)

        for key, value in constants.FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES.items():
            if key in header:
                parameters[value] = header[key]

        # The following line of code are to further process the data extracted.
        return MeasurementParser.__post_parse_measurement_parameters(parameters)

    @staticmethod
    def parse_measure_fits_file(measure_file_path):
        parameters = {'measurement_file_hash': get_file_md5(measure_file_path)}

        file_fits = fits.open(measure_file_path)
        header = file_fits[0].header

        for key, value in constants.FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES.items():
            if key in header:
                parameters[value] = header[key]

        # The following line of code are to further process the data extracted.
        return MeasurementParser.__post_parse_measurement_parameters(parameters)

    @staticmethod
    def __post_parse_measurement_parameters(parameters):

        # Date formatting

        if 'start_datetime' in parameters:
            parameters['start_datetime'] = re.sub("\+.*", "", parameters['start_datetime'].replace("T", " "))

        if 'end_datetime' in parameters:
            parameters['end_datetime'] = re.sub("\+.*", "", parameters['end_datetime'].replace("T", " "))

        return parameters
