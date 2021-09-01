# Internal dependencies
from db_irsol.api_gateway.default_gateway import DefaultGateway
from db_irsol.api_gateway.authenticate_gateway import AuthenticateGateway
from db_irsol.parsers.measurement_parser import MeasurementParser
from db_irsol.settings import Settings
from db_irsol.entities.utility import unzip_file
from db_irsol.entities.default_entity import DefaultEntity

# libraries dependencies
import os
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count


class Measurement:

    @staticmethod
    def get_measurement_from_z3bd_file(measurement_file_path, default_gateway=None):

        file_path = measurement_file_path

        if ".gz" in measurement_file_path:
            file_path = unzip_file(measurement_file_path)

        parameters = MeasurementParser.parse_z3db_file(file_path)

        path_split = measurement_file_path.split(".")
        path_split.pop()
        parameters["name"] = os.path.basename(os.path.normpath(''.join(path_split).replace("_mmd", "")))

        measurement = DefaultEntity(default_gateway if default_gateway is not None and
                                                       default_gateway.get_entry_point() == "Measurement.php" else None)
        measurement.set_parameters(parameters)

        if ".gz" in measurement_file_path:
            os.remove(file_path)

        return measurement

    @staticmethod
    def get_measurement_from_fits_file(measurement_file_path, default_gateway=None):

        file_path = measurement_file_path

        if ".gz" in measurement_file_path:
            file_path = unzip_file(measurement_file_path)

        parameters = MeasurementParser.parse_fits_file(file_path)

        path_split = measurement_file_path.split(".")
        path_split.pop()
        parameters["name"] = os.path.basename(os.path.normpath(''.join(path_split)))

        measurement = DefaultEntity(default_gateway if default_gateway is not None and
                                                       default_gateway.get_entry_point() == "Measurement.php" else None)
        measurement.set_parameters(parameters)

        if ".gz" in measurement_file_path:
            os.remove(file_path)

        return measurement

    @staticmethod
    def get_measurements_from_observation_id(id_observation, default_gateway=None):

        measurements = set()
        measurement_gateway = DefaultGateway("Measurement.php", AuthenticateGateway(Settings.AUTHENTICATE_USERNAME,
                                                                                    Settings.AUTHENTICATE_PASSWORD))

        results = measurement_gateway.get_by_parameters({"fk_observation": id_observation})

        if results is not None:
            for measurement_parameters in results:
                measurement = DefaultEntity(default_gateway)
                measurement.set_parameters(measurement_parameters, True)
                measurements.add(measurement)

        return measurements

    @staticmethod
    def get_measurements_from_dir(directory_measurement_path, only_mmd_file=False, default_gateway=None):

        print(default_gateway)

        measurements_z3bd_files = []
        measurements_fits_files = []
        measurements = set()

        for root, directories, files in os.walk(directory_measurement_path):
            for file in files:
                # Path of the measurement
                measurement_file_path = os.path.join(root, file)
                # Check if the measurement contains a ignore keyword in the name
                if not any(substring in file for substring in Settings.measurements_ignore_keys_words):
                    if ".z3bd" in file:
                        if only_mmd_file and "_mmd" in file:
                            measurements_z3bd_files.append(measurement_file_path)
                        elif not only_mmd_file:
                            measurements_z3bd_files.append(measurement_file_path)
                    elif ".fits" in file:
                        measurements_fits_files.append(measurement_file_path)

        pool = Pool(cpu_count())

        print(measurements_z3bd_files)

        for measurement in measurements_z3bd_files:
            pool.apply_async(Measurement.get_measurement_from_z3bd_file, (measurement, default_gateway,),
                             callback=measurements.add)

        for measurement in measurements_fits_files:
            pool.apply_async(Measurement.get_measurement_from_fits_file, (measurement, default_gateway),
                             callback=measurements.add)

        pool.close()
        pool.join()

        return measurements
