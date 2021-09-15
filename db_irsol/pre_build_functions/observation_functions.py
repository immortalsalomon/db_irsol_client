# Internal dependencies
from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.entity_manager import EntityManager
from db_irsol.entities.entities.default_entity import DefaultEntity
from db_irsol.settings import Settings

# libraries dependencies
import os
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
import copy


class ObservationFunctions:

    ##########################################################
    ### Pre build functions to get table Observation info  ###
    ##########################################################

    # This function returns the information of each columns present in the Observation table in the database.
    @staticmethod
    def get_info_observation_table_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_info_table_columns(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the names of each columns present in the Observation table in the database.
    @staticmethod
    def get_names_observation_table_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_table_columns_names(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the information of each not null columns present in the Observation table in the database.
    @staticmethod
    def get_info_observation_table_not_null_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_info_table_not_null_columns(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the names of each not null columns present in the Observation table in the database.
    @staticmethod
    def get_names_observation_table_not_null_columns(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_table_not_null_columns_names(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the name of the id column (identification column) present in
    # the Observation table in the database.
    @staticmethod
    def get_name_observation_table_column_id(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_table_column_id_name(
            gateway_manager.get_authenticate_gateway())

        return to_return

    # This function returns the number of records present in the Observation table in the database.
    @staticmethod
    def get_number_of_records_observation_table(gateway_manager=None):

        if not isinstance(gateway_manager, GatewayManager):
            gateway_manager = GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        to_return = gateway_manager.get_default_gateway('Observation.php').get_number_of_elements(
            gateway_manager.get_authenticate_gateway())

        return to_return

    ####################################################
    ### Pre build functions to retrieve Observation  ###
    ####################################################

    # This function returns an observation from the passed observation folder.
    @staticmethod
    def get_observation_from_dir(observation_dir_path):
        observation, _ = ObservationFunctions.get_observation_and_measurements_from_dir(observation_dir_path)
        return observation

    # This function returns all the observation present in the passed folder.
    @staticmethod
    def get_observations_from_dir(observations_dir_path):
        observations, _ = ObservationFunctions.get_observations_and_measurements_from_dir(observations_dir_path)
        return observations

    # This function returns an observation and its measurements from the passed observation folder.
    @staticmethod
    def get_observation_and_measurements_from_dir(observation_dir_path):
        observation = None
        measurements = None

        if os.path.exists(observation_dir_path):
            observation, measurements = EntityManager.get_observation_and_measurements_from_dir(observation_dir_path)
        else:
            print("Observation dir not found.")

        return observation, measurements

    # This function returns all the observations and their measurements from the passed folder.
    @staticmethod
    def get_observations_and_measurements_from_dir(observations_dir_path):
        observations = set()
        ob_measurements = {}

        if os.path.exists(observations_dir_path):
            for observation_dir_path in os.listdir(observations_dir_path):
                ob_path = os.path.join(observations_dir_path, observation_dir_path)
                observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(ob_path)
                observations.add(observation)
                ob_measurements[hash(observation)] = measurements
        else:
            print("Observations dir not found.")

        return observations, ob_measurements

    # This function returns a record with the same passed id, if it is present in the Observation table in the database.
    @staticmethod
    def get_observation_by_id_from_server(identification_number, gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(identification_number, int):
            print("The identification_number parameter is not a number")
        else:
            to_return = entity_manager.get_entity_by_id_from_server(identification_number, 'Observation.php')

        return to_return

    # This function returns a range, specified by the passed parameters, of records
    # present in the Observation table in the database. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_observations_chunk_from_server(start_element_number, number_of_elements, gateway_manager=None):

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
                                                                      'Observation.php')

        return to_return

    # This function returns all the records present in the Observation table in the database
    # that match the passed parameters.
    @staticmethod
    def get_observations_by_parameters_from_server(parameters, gateway_manager=None):

        to_return = None

        if isinstance(gateway_manager, GatewayManager):
            entity_manager = EntityManager(gateway_manager)
        else:
            entity_manager = EntityManager(GatewayManager(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD))

        if not isinstance(parameters, dict):
            print("The parameters parameter is not a dictionary")
        else:
            to_return = entity_manager.get_entities_by_parameters_from_server(parameters, 'Observation.php')

        return to_return

        # This function returns all the records present in the Observation table in the database
        # that match the passed parameters.

    # This function returns a range of records present in the Observation table in the database
    # that match the passed parameters. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_observations_chunk_by_parameters_from_server(start_element_number, number_of_elements, parameters,
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
                                                                                    parameters, 'Observation.php')

        return to_return

    ##################################################
    ### Pre build functions to insert Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def insert_observation_on_server(observation, gateway_manager):
        result = None

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(observation, DefaultEntity):
            print("You need to provide a valid observation. Observation parameter is an DefaultEntity object.")
        else:
            entity_manager = EntityManager(gateway_manager)
            result = entity_manager.insert(observation)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def insert_observations_on_server(observations, gateway_manager):
        results = None

        if not isinstance(observations, set) and not isinstance(observations, list):
            print("The observations parameter is not a list or a set.")
        else:
            results = {}
            for observation in observations:
                result = ObservationFunctions.insert_observation_on_server(observation, gateway_manager)
                results[hash(observation)] = result

        return results

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def insert_observation_on_server_from_dir(observation_dir_path, gateway_manager):

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path)
        result = ObservationFunctions.insert_observation_on_server(observation, gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def insert_observations_on_server_from_dir(observations_dir_path, gateway_manager):

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path)
        result = ObservationFunctions.insert_observations_on_server(observations, gateway_manager)

        return result

    # This function allows to insert on the server an observation and its measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server(observation, measurements, gateway_manager):

        entity_manager = EntityManager(gateway_manager)

        result = ObservationFunctions.insert_observation_on_server(observation, gateway_manager)

        if result is None and isinstance(observation, DefaultEntity):
            entity_manager.synchronize_entity_with_server(observation)
            if observation.is_entity_synchronized_with_server():
                result = observation.get_parameters()['id_observation']

        if result is None:
            print("Can't add the observation and can't find the observation on the database.")
        elif measurements is None:
            print("The parameter measurements passed is None.")
        elif not isinstance(measurements, list) and not isinstance(measurements, set):
            print("The measurements parameter need to be a list or a set.")
        elif all(isinstance(measurement, DefaultEntity) for measurement in measurements):
            pool = Pool(cpu_count())
            for measurement in measurements:
                measurement.add_parameters({'fk_observation': result})
                pool.apply_async(entity_manager.insert, (measurement, ))

            pool.close()
            pool.join()
        else:
            print("One or more measurement in the measurements are not instance of the class DefaultEntity.")

        return result

    # This function allows to insert on the server some observations and theirs measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server(observations, measurements, gateway_manager):
        result = None

        if observations is None:
            print("The observations parameter is None.")
        if not isinstance(observations, list) and not isinstance(observations, set):
            print("The observations parameter need to be a list or a set.")
        elif measurements is None:
            print("The measurements parameter is None.")
        if not isinstance(measurements, dict):
            print("The measurements parameter need to be a dictionary.")
        else:
            result = {}
            for observation in observations:
                result[hash(observation)] = ObservationFunctions.insert_observation_and_measurements_on_server(
                    observation, measurements[hash(observation)], gateway_manager)

        return result

    # This function allows to insert on the server an observation and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server_from_dir(observation_dir_path, gateway_manager):

        observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(
            observation_dir_path)
        result = ObservationFunctions.insert_observation_and_measurements_on_server(observation, measurements,
                                                                                    gateway_manager)

        return result

    # This function allows to insert on the server some observations and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server_from_dir(observations_dir_path, gateway_manager):

        observations, measurements = ObservationFunctions.get_observations_and_measurements_from_dir(
            observations_dir_path)
        result = ObservationFunctions.insert_observations_and_measurements_on_server(observations, measurements,
                                                                                     gateway_manager)
        return result

    ##################################################
    ### Pre build functions to update Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def update_observation_on_server(observation, parameters_to_update, gateway_manager):
        result = None

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(observation, DefaultEntity):
            print("You need to provide a valid observation. Observation parameter is an DefaultEntity object.")
        elif parameters_to_update is None:
            print("The parameters_to_update parameter is None.")
        elif not isinstance(parameters_to_update, dict):
            print("The parameter parameters_to_update need to be a dictionary.")
        else:
            entity_manager = EntityManager(gateway_manager)

            if not observation.is_entity_synchronized_with_server():
                entity_manager.synchronize_entity_with_server(observation)

            if observation.is_entity_synchronized_with_server():
                result = entity_manager.update(observation, parameters_to_update)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def update_observations_on_server(observations, parameters_to_update, gateway_manager):
        result = None

        if observations is None:
            print("The observations parameter is None.")
        if not isinstance(observations, set) and not isinstance(observations, list):
            print("The parameter observations need to be a list or a set.")
        if not all(isinstance(observation, DefaultEntity) for observation in observations):
            print("Not all observations in the observations set/list are instance of the DefaultEntity class.")
        elif parameters_to_update is None:
            print("The parameters_to_update parameter is None.")
        elif not isinstance(parameters_to_update, dict):
            print("The parameter parameters_to_update need to be a dictionary.")
        if not all(isinstance(parameters, dict) for parameters in parameters_to_update.values()):
            print("Not all the value of the parameter parameters_to_update are dictionary.")
        else:
            result = {}
            for observation in observations:
                if hash(observation) in parameters_to_update:
                    result[hash(observation)] = ObservationFunctions.update_observation_on_server(
                        observation, parameters_to_update[hash(observation)], gateway_manager)

        return result

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def update_observation_on_server_from_dir(observation_dir_path, gateway_manager):
        result = None

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path)

        if not isinstance(observation, DefaultEntity):
            print("You need to provide a valid observation. Observation parameter is an DefaultEntity object.")
        else:
            parameters_to_update = copy.deepcopy(observation.get_parameters())
            result = ObservationFunctions.update_observation_on_server(observation, parameters_to_update,
                                                                       gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def update_observations_on_server_from_dir(observations_dir_path, gateway_manager):
        result = None

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path)

        if not isinstance(observations, set) and not isinstance(observations, list):
            print("Can't find any observation in the passed directory.")
        else:
            parameters_to_update = {}

            for observation in observations:
                parameters_to_update[hash(observation)] = copy.deepcopy(observation.get_parameters())

            result = ObservationFunctions.update_observations_on_server(observations, parameters_to_update,
                                                                        gateway_manager)

        return result

    ##################################################
    ### Pre build functions to delete Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def delete_observation_on_server(observation, gateway_manager):
        result = False

        if not isinstance(gateway_manager, GatewayManager):
            print("You need to provide a gateway_manager to connect with the service REST API.")
        elif not isinstance(observation, DefaultEntity):
            print("You need to provide a valid observation. Observation parameter is an DefaultEntity object.")
        else:
            entity_manager = EntityManager(gateway_manager)

            if not observation.is_entity_synchronized_with_server():
                entity_manager.synchronize_entity_with_server(observation)

            if observation.is_entity_synchronized_with_server():
                result = entity_manager.delete(observation)

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def delete_observations_on_server(observations, gateway_manager):
        result = None

        if observations is None:
            print("The observations parameter is None.")
        if not isinstance(observations, set) and not isinstance(observations, list):
            print("The parameter observations need to be a set or a list.")
        if not all(isinstance(observation, DefaultEntity) for observation in observations):
            print("Not all the observations in observations parameter are instance of the class DefaultEntity.")
        else:
            result = {}
            for observation in observations:
                result[hash(observation)] = ObservationFunctions.delete_observation_on_server(observation,
                                                                                              gateway_manager)
        return result

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def delete_observation_on_server_from_dir(observation_dir_path, gateway_manager):

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path)
        result = ObservationFunctions.delete_observation_on_server(observation, gateway_manager)

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def delete_observations_on_server_from_dir(observations_dir_path, gateway_manager):

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path)
        result = ObservationFunctions.delete_observations_on_server(observations, gateway_manager)

        return result
