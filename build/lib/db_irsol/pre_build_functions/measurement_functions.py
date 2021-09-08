# Internal dependencies
from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.entity_manager import EntityManager
from db_irsol.entities.entities.default_entity import DefaultEntity
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions
from db_irsol.settings import Settings

# libraries dependencies
import os
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
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

    # This function returns measurements from the passed folder.
    @staticmethod
    def get_measurements_from_dir(dir_path):
        measurements = None

        if not os.path.exists(dir_path):
            print("dir not found.")
        else:
            measurements = EntityManager.get_measurements_from_dir(dir_path)

        return measurements

    # This function returns all the measurement present in the passed folder.
    @staticmethod
    def get_measurements_from_dirs(dirs_path):

        measurements = None

        if not isinstance(dirs_path, list):
            print("The dirs_path is not a list of directory path.")
        else:
            measurements = {}
            for dir_path in dirs_path:
                measurements[dir_path] = MeasurementFunctions.get_measurements_from_dir(dir_path)

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
