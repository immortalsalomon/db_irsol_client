# Internal dependencies
from db_irsol.parsers.utility import filter_string_parameters


class LogParser:

    # Parser for log file from 2020 or later.
    # Coded year 2021
    @staticmethod
    def parse_log_file_first(log_file_path):
        parameters = {}
        # Open file and read all lines
        log = open(log_file_path, 'r')
        lines = log.readlines()

        # Get project
        parameters["project"] = lines[0].replace('<TITLE>', '').strip()

        # Get weather condition
        parameters["weather_condition"] = lines[5].replace('-', ' ').replace('<WEATHER>', ' ').strip()

        # Get seeing condition
        parameters["seeing_condition"] = lines[6].replace('-', ' ').replace('<SEEING>', ' ').strip()

        # Get sun condition
        parameters["sun_condition"] = lines[7].replace('-', ' ').replace('<SUN>', ' ').strip()

        # Get telescope
        parameters["fk_telescope-name"] = lines[11].rpartition(':')[2].strip()

        # Get setup, instrument and pfinstrument
        instrument_pfinstrument_setup = lines[12].rpartition('with')
        parameters["setup"] = instrument_pfinstrument_setup[0].replace('-', ' ').strip()

        instrument_pfinstrument = instrument_pfinstrument_setup[2].rpartition('and')
        # Get instrument
        parameters["fk_instrument-name"] = instrument_pfinstrument[0].strip()
        parameters["fk_pfinstrument-name"] = instrument_pfinstrument[2].strip()

        # Get modulator and optics
        modulator_optics = lines[13].rpartition('with')
        parameters["fk_modulator-name"] = modulator_optics[0].replace('- Modulator', ' ').strip()
        parameters["fk_optic-name"] = modulator_optics[2].replace('optics', ' ').strip()

        parameters = filter_string_parameters(parameters)

        return parameters
