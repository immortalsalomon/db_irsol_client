# Internal dependencies
from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.entity_manager import EntityManager
from db_irsol.entities.entities.default_entity import DefaultEntity
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions
from db_irsol.settings import Settings

# libraries dependencies
import os
import copy


class MeasurementFunctions:

    ##########################################################
    ### Pre build functions to get table Measurement info  ###
    ##########################################################

    # This function returns the information of each columns present in the Measurement table in the database.
    @staticmethod
    def get_info_measurement_table_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_info_table_columns(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the names of each columns present in the Measurement table in the database.
    @staticmethod
    def get_names_measurement_table_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_table_columns_names(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the information of each not null columns present in the Measurement table in the database.
    @staticmethod
    def get_info_measurement_table_not_null_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_info_table_not_null_columns(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the names of each not null columns present in the Measurement table in the database.
    @staticmethod
    def get_names_measurement_table_not_null_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_table_not_null_columns_names(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the name of the id column (identification column) present in
    # the Measurement table in the database.
    @staticmethod
    def get_name_measurement_table_column_id(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_table_column_id_name(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the number of records present in the Measurement table in the database.
    @staticmethod
    def get_number_of_records_measurement_table(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Measurement.php').get_number_of_elements(
            gateway_manager.get_authenticate_gateway())

        return to_return

    ####################################################
    ### Pre build functions to retrieve Measurement  ###
    ####################################################

    @staticmethod
    def get_measurement_from_file(measurement_file_path):

        measurement = None

        if not os.path.exists(measurement_file_path):
            print("The measurement file path doesn't exists. Please provide a valid path.")
        elif "z3bd" in measurement_file_path:
            measurement = EntityManager.get_measurement_from_z3bd_file(measurement_file_path)
        elif "fits" in measurement_file_path:
            measurement = EntityManager.get_measurement_from_fits_file(measurement_file_path)
        else:
            print("The format of the measurement file is not supported. Please provide z3bd or fits file. ")

        return measurement

    # This function returns measurements from the passed folder.
    @staticmethod
    def get_measurements_from_dir(dir_path):
        measurements = None

        if not os.path.exists(dir_path):
            print("Measurement dir not found.")
        else:
            measurements = EntityManager.get_measurements_from_dir(dir_path)

        return measurements

    # This function returns all the measurement present in the passed folder.
    @staticmethod
    def get_measurements_from_dirs(dirs_path):

        measurements = None

        if not isinstance(dirs_path, list):
            print("The dirs_path is not a list of directory path.")
        if not all(os.path.exists(measurement_path) for measurement_path in dirs_path):
            print("One or more path defined inside the dirs_path parameters don't exist.")
        else:
            measurements = set()
            for dir_path in dirs_path:
                measurements = measurements.union(MeasurementFunctions.get_measurements_from_dir(dir_path))

        return measurements

    # This function returns an observation and its measurements from the passed Measurement folder.
    @staticmethod
    def get_observation_and_measurements_from_dir(observation_dir_path):
        return ObservationFunctions.get_observation_and_measurements_from_dir(observation_dir_path)

    # This function returns all the observations and their measurements from the passed folder.
    @staticmethod
    def get_observations_and_measurements_from_dir(observations_dir_path):
        return ObservationFunctions.get_observations_and_measurements_from_dir(observations_dir_path)

    # This function returns a record with the same passed id, if it is present in the Measurement table in the database.
    @staticmethod
    def get_measurement_by_id_from_server(identification_number, gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(identification_number, int):
            print("The identification_number parameter is not a number")
        else:
            to_return = entity_manager.get_entity_by_id_from_server(identification_number, 'Measurement.php')

        return to_return

    # This function returns a range, specified by the passed parameters, of records
    # present in the Measurement table in the database. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_measurements_chunk_from_server(start_element_number, number_of_elements, gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(start_element_number, int):
            print("The start_element_number parameter is not a number")
        elif not isinstance(number_of_elements, int):
            print("The number_of_elements parameter is not a number")
        else:
            to_return = entity_manager.get_entities_chunk_from_server(start_element_number, number_of_elements,
                                                                      'Measurement.php')

        return to_return

    # This function returns all the records present in the Measurement table in the database
    # that match the passed parameters.
    @staticmethod
    def get_measurements_by_parameters_from_server(parameters, gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(parameters, dict):
            print("The parameters parameter is not a dictionary")
        else:
            to_return = entity_manager.get_entities_by_parameters_from_server(parameters, 'Measurement.php')

        return to_return

        # This function returns all the records present in the Measurement table in the database
        # that match the passed parameters.

    # This function returns a range of records present in the Measurement table in the database
    # that match the passed parameters. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_measurements_chunk_by_parameters_from_server(start_element_number, number_of_elements, parameters,
                                                         gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(start_element_number, int):
            print("The start_element_number parameter is not a number")
        elif not isinstance(number_of_elements, int):
            print("The number_of_elements parameter is not a number")
        elif not isinstance(parameters, dict):
            print("The parameters parameter is not a dictionary")
        else:
            to_return = entity_manager.get_entities_chunk_by_parameters_from_server(start_element_number,
                                                                                    number_of_elements,
                                                                                    parameters, 'Measurement.php')

        return to_return

    ##################################################
    ### Pre build functions to insert Measurement  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def insert_measurement_on_server(measurement, gateway_manager):
        result = None

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(measurement, DefaultEntity):
            print("You need to provide a valid measurement. Measurement parameter is an DefaultEntity object.")
        else:
            entity_manager = EntityManager(gateway_manager)
            result = entity_manager.insert(measurement)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def insert_measurements_on_server(measurements, gateway_manager):
        results = None

        if not isinstance(measurements, set) and not isinstance(measurements, list):
            print("The measurements parameter is not a list or a set.")
        else:
            results = {}
            for measurement in measurements:
                result = MeasurementFunctions.insert_measurement_on_server(measurement, gateway_manager)
                results[hash(measurement)] = result

        return results

    @staticmethod
    def insert_measurement_on_server_from_file(measurement_file_path, id_observation, gateway_manager):

        result = None

        if not isinstance(id_observation, int):
            print("The parameter id_observation is not a number.")
        else:
            measurement = MeasurementFunctions.get_measurement_from_file(measurement_file_path)

            if measurement is not None:
                measurement.add_parameters({"fk_observation": id_observation})
                result = MeasurementFunctions.insert_measurement_on_server(measurement, gateway_manager)

        return result

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def insert_measurements_on_server_from_dir(measurements_dir_path, id_observation, gateway_manager):

        result = None

        if not isinstance(id_observation, int):
            print("The parameter id_observation is not a number.")
        if not os.path.exists(measurements_dir_path):
            print("The parameter measurements_dir_path doesn't contain a valid path.")
        else:
            measurements = MeasurementFunctions.get_measurements_from_dir(measurements_dir_path)

            for measurement in measurements:
                measurement.add_parameters({"fk_observation": id_observation})

            result = MeasurementFunctions.insert_measurements_on_server(measurements, gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def insert_measurements_on_server_from_dirs(measurements_dirs_paths, id_observation, gateway_manager):

        if not isinstance(id_observation, int):
            print("The parameter id_observation is not a number.")
        else:

            measurements = MeasurementFunctions.get_measurements_from_dirs(measurements_dirs_paths)

            for measurement in measurements:
                measurement.add_parameters({"fk_observation": id_observation})

            result = MeasurementFunctions.insert_measurements_on_server(measurements, gateway_manager)

        return result

    # This function allows to insert on the server an observation and its measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server(observation, measurements, gateway_manager):
        return ObservationFunctions.insert_observation_and_measurements_on_server(observation, measurements,
                                                                                  gateway_manager)

    # This function allows to insert on the server some observations and theirs measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server(observations, measurements, gateway_manager):
        return ObservationFunctions.insert_observations_and_measurements_on_server(observations, measurements,
                                                                                   gateway_manager)

    # This function allows to insert on the server an observation and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server_from_dir(observation_dir_path, gateway_manager):
        return ObservationFunctions.insert_observation_and_measurements_on_server_from_dir(observation_dir_path,
                                                                                           gateway_manager)

    # This function allows to insert on the server some observations and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server_from_dir(observations_dir_path, gateway_manager):
        return ObservationFunctions.insert_observations_and_measurements_on_server_from_dir(observations_dir_path,
                                                                                            gateway_manager)

    ##################################################
    ### Pre build functions to update Measurement  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def update_measurement_on_server(measurement, parameters_to_update, gateway_manager):
        result = None

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(measurement, DefaultEntity):
            print("You need to provide a valid measurement. Measurement parameter is an DefaultEntity object.")
        elif parameters_to_update is None:
            print("The parameters_to_update parameter is None.")
        elif not isinstance(parameters_to_update, dict):
            print("The parameter parameters_to_update need to be a dictionary.")
        else:
            entity_manager = EntityManager(gateway_manager)

            if not measurement.is_entity_synchronized_with_server():
                entity_manager.synchronize_entity_with_server(measurement)

            if measurement.is_entity_synchronized_with_server():
                result = entity_manager.update(measurement, parameters_to_update)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def update_measurements_on_server(measurements, parameters_to_update, gateway_manager):
        result = None

        if measurements is None:
            print("The measurements parameter is None.")
        if not isinstance(measurements, set) and not isinstance(measurements, list):
            print("The parameter measurements need to be a list or a set.")
        if not all(isinstance(measurement, DefaultEntity) for measurement in measurements):
            print("Not all measurements in the measurements set/list are instance of the DefaultEntity class.")
        elif parameters_to_update is None:
            print("The parameters_to_update parameter is None.")
        elif not isinstance(parameters_to_update, dict):
            print("The parameter parameters_to_update need to be a dictionary.")
        if not all(isinstance(parameters, dict) for parameters in parameters_to_update.values()):
            print("Not all the value of the parameter parameters_to_update are dictionary.")
        else:
            result = {}
            for measurement in measurements:
                if hash(measurement) in parameters_to_update:
                    result[hash(measurement)] = MeasurementFunctions.update_measurement_on_server(
                        measurement, parameters_to_update[hash(measurement)], gateway_manager)

        return result

    @staticmethod
    def update_measurement_on_server_from_file(measurement_file_path, gateway_manager):

        result = None

        if not os.path.exists(measurement_file_path):
            print("The parameter measurement_file_path doesn't contain a valid path.")
        else:
            measurement = MeasurementFunctions.get_measurement_from_file(measurement_file_path)
            parameters_to_update = copy.deepcopy(measurement.get_parameters())

            result = MeasurementFunctions.update_measurement_on_server(measurement, parameters_to_update,
                                                                       gateway_manager)

        return result

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def update_measurements_on_server_from_dir(measurements_dir_path, gateway_manager):

        result = None

        measurements = MeasurementFunctions.get_measurements_from_dirs(measurements_dir_path)

        if not isinstance(measurements, set) and not isinstance(measurements, list):
            print("Can't find measurements in the passed folder.")
        else:
            parameters_to_update = {}

            for measurement in measurements:
                parameters_to_update[hash(measurement)] = copy.deepcopy(measurement.get_parameters())

            result = MeasurementFunctions.update_measurements_on_server(measurements, parameters_to_update,
                                                                        gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def update_measurements_on_server_from_dirs(observations_dirs_paths, gateway_manager):

        result = None

        measurements = MeasurementFunctions.get_measurements_from_dirs(observations_dirs_paths)

        if not isinstance(measurements, set) and not isinstance(measurements, list):
            print("Can't find any measurements in the passed directory.")
        else:
            parameters_to_update = {}

            for measurement in measurements:
                parameters_to_update[hash(measurement)] = copy.deepcopy(measurement.get_parameters())

            result = MeasurementFunctions.update_measurements_on_server(measurements, parameters_to_update,
                                                                        gateway_manager)

        return result

    ##################################################
    ### Pre build functions to delete Measurement  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def delete_measurement_on_server(measurement, gateway_manager):
        result = False

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(measurement, DefaultEntity):
            print("You need to provide a valid measurement. Measurement parameter is an DefaultEntity object.")
        else:
            entity_manager = EntityManager(gateway_manager)

            if not measurement.is_entity_synchronized_with_server():
                entity_manager.synchronize_entity_with_server(measurement)

            if measurement.is_entity_synchronized_with_server():
                result = entity_manager.delete(measurement)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def delete_measurements_on_server(measurements, gateway_manager):
        result = None

        if not isinstance(measurements, set) and not isinstance(measurements, list):
            print("The parameter measurements need to be a set or a list.")
        if not all(isinstance(measurement, DefaultEntity) for measurement in measurements):
            print("Not all the measurements in measurements parameter are instance of the class DefaultEntity.")
        else:
            result = {}
            for measurement in measurements:
                result[hash(measurement)] = MeasurementFunctions.delete_measurement_on_server(measurement,
                                                                                              gateway_manager)
        return result

    @staticmethod
    def delete_measurement_on_server_from_file(measurement_file_path, gateway_manager):

        measurement = MeasurementFunctions.get_measurement_from_file(measurement_file_path)
        result = MeasurementFunctions.delete_measurement_on_server(measurement, gateway_manager)

        return result

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def delete_measurements_on_server_from_dir(measurements_dir_path, gateway_manager):

        measurements = MeasurementFunctions.get_measurements_from_dir(measurements_dir_path)
        result = MeasurementFunctions.delete_measurements_on_server(measurements, gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def delete_measurements_on_server_from_dirs(observations_dirs_paths, gateway_manager):

        measurements = MeasurementFunctions.get_measurements_from_dirs(observations_dirs_paths)
        result = MeasurementFunctions.delete_measurements_on_server(measurements, gateway_manager)

        return result
