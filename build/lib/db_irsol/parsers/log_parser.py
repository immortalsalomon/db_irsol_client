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
        counter = 0
        for line in lines:

            if "Conditions" in line:
                # Get weather condition
                parameters["weather_condition"] = lines[counter + 2].replace('-', ' ').replace('<WEATHER>', ' ')\
                    .rpartition(':')[2].strip()

                # Get seeing condition
                parameters["seeing_condition"] = lines[counter + 3].replace('-', ' ').replace('<SEEING>', ' ')\
                    .rpartition(':')[2].strip()

                # Get sun condition
                parameters["sun_condition"] = lines[counter + 4].replace('-', ' ').replace('<SUN>', ' ')\
                    .rpartition(':')[2].strip()

            elif "Instrument Setup" in line:
                # Get telescope
                parameters["fk_telescope-name"] = lines[counter + 2].rpartition(':')[2].strip()

                # Get setup, instrument and pfinstrument
                instrument_pfinstrument_setup = lines[counter + 3].rpartition('with')
                parameters["setup"] = instrument_pfinstrument_setup[0].replace('-', ' ').strip()

                instrument_pfinstrument = instrument_pfinstrument_setup[2].rpartition('and')
                # Get instrument
                parameters["fk_instrument-name"] = instrument_pfinstrument[0].strip()
                parameters["fk_pfinstrument-name"] = instrument_pfinstrument[2].strip()

                # Get modulator and optics
                modulator_optics = lines[counter + 4].rpartition('with')
                parameters["fk_modulator-name"] = modulator_optics[0].replace('- Modulator', ' ').strip()
                parameters["fk_optic-name"] = modulator_optics[2].replace('optics', ' ').strip()

            counter += 1

        parameters = filter_string_parameters(parameters)

        return parameters
