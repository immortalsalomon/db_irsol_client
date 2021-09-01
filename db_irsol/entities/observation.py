# Internal dependencies
from db_irsol.entities.default_entity import DefaultEntity
from db_irsol.parsers.log_parser import LogParser
from db_irsol.entities.measurement import Measurement

# libraries dependencies
import os
import re


class Observation:

    @staticmethod
    def get_observation_and_measurements_from_dir(directory_observation_path, manager_gateway=None):

        measurement_dir = directory_observation_path
        only_mmd_file = False
        parameters = dict()
        elements_in_dir = []

        try:
            elements_in_dir = os.listdir(directory_observation_path)
        except:
            return None

        # Get name of the observation
        parameters["name"] = os.path.basename(os.path.normpath(directory_observation_path))

        # Get the path of the observation
        parameters["rpath"] = directory_observation_path

        # Extract the date and add datetime
        date_match = re.search("^[0-9]{6,8}", parameters["name"])
        date_string = date_match.group()
        date = [date_string[i:i + 2] for i in range(0, len(date_string), 2)]

        datetime = ""
        if len(date) == 3:
            datetime = "20" + date[0] + "-" + date[1] + "-" + date[2] + " 00:00:00"
        else:
            datetime = date[0] + date[1] + "-" + date[2] + "-" + date[3] + " 00:00:00"

        parameters["datetime"] = datetime

        # Check if the measurement file are mmd with z3bd extension
        for path, subdirs, files in os.walk(directory_observation_path):
            for file in files:
                if "_mmd.z3bd" in file:
                    only_mmd_file = True
                    break

        # select the procedure based on the structure of the observation folder
        if only_mmd_file:
            if "_log" in elements_in_dir:
                # Get file log from observation directory
                log_file_dir = os.path.join(directory_observation_path, "_log")
                log_file = os.listdir(log_file_dir)[0]
                log_file_path = os.path.join(log_file_dir, log_file)

                parameters = {**parameters, **LogParser.parse_log_file_first(log_file_path)}
        elif "raw" in elements_in_dir:
            measurement_dir = os.path.join(directory_observation_path, "raw")

        measurements = Measurement.get_measurements_from_dir(measurement_dir, only_mmd_file,
                                                             manager_gateway.get_default_gateway('Measurement.php')
                                                             if manager_gateway is not None else None)

        observation = None

        # Get telescope name if not in log file
        if "fk_telescope-name" not in parameters.keys():
            for measurement in measurements:
                if "fk_telescope-name" in measurement.parameters:
                    parameters["fk_telescope-name"] = measurement.parameters["fk_telescope-name"]
                    break

        if "fk_telescope-name" in parameters.keys():
            observation = DefaultEntity(manager_gateway.get_default_gateway('Observation.php')
                                        if manager_gateway is not None else None)
            observation.set_parameters(parameters)

        return observation, measurements
