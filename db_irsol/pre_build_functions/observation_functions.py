# Internal dependencies
from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.observation import Observation
from db_irsol.entities.default_entity import DefaultEntity

# libraries dependencies
import os
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count


# if os.path.exists(name):
class ObservationFunctions:

    ##########################################################
    ### Pre build functions to get table Observation info  ###
    ##########################################################

    # This function returns the information of each columns present in the Observation table in the database.
    @staticmethod
    def get_info_observation_table_columns(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_info_table_columns()

        return to_return

    # This function returns the names of each columns present in the Observation table in the database.
    @staticmethod
    def get_names_observation_table_columns(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_table_columns_names()

        return to_return

    # This function returns the information of each not null columns present in the Observation table in the database.
    @staticmethod
    def get_info_observation_table_not_null_columns(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_info_table_not_null_columns()

        return to_return

    # This function returns the names of each not null columns present in the Observation table in the database.
    @staticmethod
    def get_names_observation_table_not_null_columns(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_table_not_null_columns_names()

        return to_return

    # This function returns the name of the id column (identification column) present in
    # the Observation table in the database.
    @staticmethod
    def get_name_observation_table_column_id(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_table_column_id_name()

        return to_return

    # This function returns the number of records present in the Observation table in the database.
    @staticmethod
    def get_number_of_records_observation_table(manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_number_of_elements()

        return to_return

    ####################################################
    ### Pre build functions to retrieve Observation  ###
    ####################################################

    # This function returns an observation from the passed observation folder.
    @staticmethod
    def get_observation_from_dir(observation_dir_path, manager_gateway=None):
        observation, _ = ObservationFunctions.get_observation_and_measurements_from_dir(observation_dir_path,
                                                                                        manager_gateway)

        return observation

    # This function returns all the observation present in the passed folder.
    @staticmethod
    def get_observations_from_dir(observations_dir_path, manager_gateway=None):
        observations, _ = ObservationFunctions.get_observations_and_measurements_from_dir(observations_dir_path,
                                                                                          manager_gateway)

        return observations

    # This function returns an observation and its measurements from the passed observation folder.
    @staticmethod
    def get_observation_and_measurements_from_dir(observation_dir_path, manager_gateway=None):
        observation, measurements = Observation.get_observation_and_measurements_from_dir(observation_dir_path,
                                                                                          manager_gateway)

        return observation, measurements

    # This function returns all the observations and their measurements from the passed folder.
    @staticmethod
    def get_observations_and_measurements_from_dir(observations_dir_path, manager_gateway=None):
        observations = set()
        ob_measurements = {}

        for observation_dir_path in os.listdir(observations_dir_path):
            ob_path = os.path.join(observations_dir_path, observation_dir_path)
            observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(ob_path,
                                                                                                       manager_gateway)
            observations.add(observation)
            ob_measurements[hash(observation)] = measurements

        return observations, ob_measurements

    # This function returns a record with the same passed id, if it is present in the Observation table in the database.
    @staticmethod
    def get_observation_by_id_on_server(identification_number, manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_by_id(identification_number)

        return to_return

    # This function returns a range, specified by the passed parameters, of records
    # present in the Observation table in the database. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_observations_chunk_on_server(start_element_number, number_of_elements, manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_chunk(start_element_number,
                                                                                         number_of_elements)

        return to_return

    # This function returns all the records present in the Observation table in the database
    # that match the passed parameters.
    @staticmethod
    def get_observations_by_parameters_on_server(parameters, manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_by_parameters(parameters)

        return to_return

        # This function returns all the records present in the Observation table in the database
        # that match the passed parameters.

    # This function returns a range of records present in the Observation table in the database
    # that match the passed parameters. Before retrieve the specified range the query on the server
    # sorts the records based on the id (identification value). This allows to retrieve always the same records
    # with the same range parameters, if no actions are executed on the database.
    @staticmethod
    def get_observations_chunk_by_parameters_on_server(start_element_number, number_of_elements, parameters,
                                                       manager_gateway):
        to_return = None

        if isinstance(manager_gateway, GatewayManager):
            to_return = manager_gateway.get_default_gateway('Observation.php').get_chunk_by_parameters(
                start_element_number, number_of_elements, parameters)

        return to_return

    ##################################################
    ### Pre build functions to insert Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def insert_observation_on_server(observation, manager_gateway=None):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):

            if manager_gateway is not None and isinstance(manager_gateway, GatewayManager):
                observation.set_default_gateway(manager_gateway.get_default_gateway("Observation.php"))

            result = observation.insert()

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def insert_observations_on_server(observations, manager_gateway=None):
        results = {}

        if observations is not None:

            for observation in observations:
                result = ObservationFunctions.insert_observation_on_server(observation, manager_gateway)
                results[result] = observation

        return results

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def insert_observation_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path, manager_gateway)

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def insert_observations_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = False

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path, manager_gateway)

        for observation in observations:
            if observation is not None and isinstance(observation, DefaultEntity):
                result = observation.insert()

        return result

    # This function allows to insert on the server an observation and its measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server(observation, measurements):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        if result is not None and measurements is not None:
            pool = Pool(cpu_count())

            for measurement in measurements:
                if isinstance(measurement, DefaultEntity):
                    measurement.add_parameters({'fk_observation': result})
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and theirs measurements,
    # if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server(observations, measurements):
        result = None

        if observations is not None and measurements is not None:
            for observation in observations:
                result = ObservationFunctions.insert_observation_and_measurements_on_server(
                    observation, measurements[hash(observation)])

        return result

    # This function allows to insert on the server an observation and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observation_and_measurements_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None
        observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(
            observation_dir_path, manager_gateway)

        if observation is not None:
            result = observation.insert()

        if result is None and observation.get_is_synchronized_with_server():
            result = observation.get_parameters()['id_observation']

        if result is not None:

            pool = Pool(cpu_count())

            for measurement in measurements:
                measurement.add_parameters({'fk_observation': result})
                if not measurement.get_is_synchronized_with_server():
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def insert_observations_and_measurements_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = None
        observations, measurements = ObservationFunctions.get_observations_and_measurements_from_dir(
            observations_dir_path, manager_gateway)

        for observation in observations:
            result = ObservationFunctions.insert_observation_and_measurements_on_server(
                observation, measurements[hash(observation)])

        return result

    ##################################################
    ### Pre build functions to update Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def update_observation_on_server(observation, manager_gateway=None):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):

            if manager_gateway is not None and isinstance(manager_gateway, GatewayManager):
                observation.set_default_gateway(manager_gateway.get_default_gateway("Observation.php"))

            result = observation.insert()

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def update_observations_on_server(observations, manager_gateway=None):
        results = {}

        if observations is not None:

            for observation in observations:
                result = ObservationFunctions.insert_observation_on_server(observation, manager_gateway)
                results[result] = observation

        return results

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def update_observation_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path, manager_gateway)

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def update_observations_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = False

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path, manager_gateway)

        for observation in observations:
            if observation is not None and isinstance(observation, DefaultEntity):
                result = observation.insert()

        return result

    # This function allows to insert on the server an observation and its measurements,
    # if they are not present on the server.
    @staticmethod
    def update_observation_and_measurements_on_server(observation, measurements):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        if result is not None and measurements is not None:
            pool = Pool(cpu_count())

            for measurement in measurements:
                if isinstance(measurement, DefaultEntity):
                    measurement.add_parameters({'fk_observation': result})
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and theirs measurements,
    # if they are not present on the server.
    @staticmethod
    def update_observations_and_measurements_on_server(observations, measurements):
        result = None

        if observations is not None and measurements is not None:
            for observation in observations:
                result = ObservationFunctions.insert_observation_and_measurements_on_server(
                    observation, measurements[hash(observation)])

        return result

    # This function allows to insert on the server an observation and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def update_observation_and_measurements_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None
        observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(
            observation_dir_path, manager_gateway)

        if observation is not None:
            result = observation.insert()

        if result is None and observation.get_is_synchronized_with_server():
            result = observation.get_parameters()['id_observation']

        if result is not None:

            pool = Pool(cpu_count())

            for measurement in measurements:
                measurement.add_parameters({'fk_observation': result})
                if not measurement.get_is_synchronized_with_server():
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def update_observations_and_measurements_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = None
        observations, measurements = ObservationFunctions.get_observations_and_measurements_from_dir(
            observations_dir_path, manager_gateway)

        for observation in observations:
            result = ObservationFunctions.insert_observation_and_measurements_on_server(
                observation, measurements[hash(observation)])

        return result

    ##################################################
    ### Pre build functions to delete Observation  ###
    ##################################################

    # This function adds the passed observation in the database, if it is not already present.
    @staticmethod
    def delete_observation_on_server(observation, manager_gateway=None):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):

            if manager_gateway is not None and isinstance(manager_gateway, GatewayManager):
                observation.set_default_gateway(manager_gateway.get_default_gateway("Observation.php"))

            result = observation.insert()

        return result

    # This function adds the passed observations in the database, if it is not already present.
    @staticmethod
    def delete_observations_on_server(observations, manager_gateway=None):
        results = {}

        if observations is not None:

            for observation in observations:
                result = ObservationFunctions.insert_observation_on_server(observation, manager_gateway)
                results[result] = observation

        return results

    # This function allows to insert in the database an observation from the passed folder,
    # if it is not already present.
    @staticmethod
    def delete_observation_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None

        observation = ObservationFunctions.get_observation_from_dir(observation_dir_path, manager_gateway)

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        return result

    # This function allows to insert on the server the observations present in the passed folder,
    # if they are not present on the server.
    @staticmethod
    def delete_observations_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = False

        observations = ObservationFunctions.get_observations_from_dir(observations_dir_path, manager_gateway)

        for observation in observations:
            if observation is not None and isinstance(observation, DefaultEntity):
                result = observation.insert()

        return result

    # This function allows to insert on the server an observation and its measurements,
    # if they are not present on the server.
    @staticmethod
    def delete_observation_and_measurements_on_server(observation, measurements):
        result = None

        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

        if result is not None and measurements is not None:
            pool = Pool(cpu_count())

            for measurement in measurements:
                if isinstance(measurement, DefaultEntity):
                    measurement.add_parameters({'fk_observation': result})
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and theirs measurements,
    # if they are not present on the server.
    @staticmethod
    def delete_observations_and_measurements_on_server(observations, measurements):
        result = None

        if observations is not None and measurements is not None:
            for observation in observations:
                result = ObservationFunctions.insert_observation_and_measurements_on_server(
                    observation, measurements[hash(observation)])

        return result

    # This function allows to insert on the server an observation and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def delete_observation_and_measurements_on_server_from_dir(observation_dir_path, manager_gateway=None):
        result = None
        observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir(
            observation_dir_path, manager_gateway)

        if observation is not None:
            result = observation.insert()

        if result is None and observation.get_is_synchronized_with_server():
            result = observation.get_parameters()['id_observation']

        if result is not None:

            pool = Pool(cpu_count())

            for measurement in measurements:
                measurement.add_parameters({'fk_observation': result})
                if not measurement.get_is_synchronized_with_server():
                    pool.apply_async(measurement.insert, ())

            pool.close()
            pool.join()

        return result

    # This function allows to insert on the server some observations and their measurements
    # present in the passed folder, if they are not present on the server.
    @staticmethod
    def delete_observations_and_measurements_on_server_from_dir(observations_dir_path, manager_gateway=None):
        result = None
        observations, measurements = ObservationFunctions.get_observations_and_measurements_from_dir(
            observations_dir_path, manager_gateway)

        for observation in observations:
            result = ObservationFunctions.insert_observation_and_measurements_on_server(
                observation, measurements[hash(observation)])

        return result
