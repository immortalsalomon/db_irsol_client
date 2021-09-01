# Internal dependencies
from db_irsol.api_gateway.authenticate_gateway import AuthenticateGateway
from db_irsol.api_gateway.default_gateway import DefaultGateway
from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.observation import Observation
from db_irsol.entities.default_entity import DefaultEntity

# libraries dependencies
import os
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count




###########################################
### Pre build functions for Observation ###
###########################################

# This function return an observation from the passed observation folder.
def get_observation_from_dir(observation_dir_path, manager_gateway=None):
    observation, _ = get_observation_and_measurements_from_dir(observation_dir_path, manager_gateway)

    return observation


# This function return all the observation present in the passed folder.
def get_observations_from_dir(observations_dir_path, manager_gateway=None):
    observations = set()

    for observation_dir_path in os.listdir(observations_dir_path):
        ob_path = os.path.join(observations_dir_path, observation_dir_path)
        observations.add(get_observation_from_dir(ob_path, manager_gateway))

    return observations


# This function return an observation and its measurements from the passed observation folder.
def get_observation_and_measurements_from_dir(observation_dir_path, manager_gateway=None):
    observation, measurements = Observation.get_observation_and_measurements_from_dir(observation_dir_path,
                                                                                      manager_gateway)

    return observation, measurements


# This function return all the observations and their measurements from the passed folder.
def get_observations_and_measurements_from_dir(observations_dir_path, manager_gateway=None):
    observations = set()
    ob_measurements = {}

    for observation_dir_path in os.listdir(observations_dir_path):
        ob_path = os.path.join(observations_dir_path, observation_dir_path)
        observation, measurements = get_observation_and_measurements_from_dir(ob_path, manager_gateway)
        observations.add(observation)
        ob_measurements[hash(observation)] = measurements

    return observations, ob_measurements


# region Insert


# This function add the passed observation to the server, if it is not present on the server.
def insert_observation_on_server(observation):
    result = None

    if observation is not None and isinstance(observation, DefaultEntity):
        result = observation.insert()

    return result


# This function add the passed observations to the server, if they are not present on the server.
def insert_observations_on_server(observations):
    result = None

    if observations is not None:
        for observation in observations:
            result = insert_observation_on_server(observation)

    return result


# This function allows to insert on the server an observation from the passed observation folder,
# if it is not present on the server.
def insert_observation_on_server_from_dir(observation_dir_path, manager_gateway=None):
    result = False

    observation = get_observation_from_dir(observation_dir_path, manager_gateway)

    if observation is not None and isinstance(observation, DefaultEntity):
        result = observation.insert()

    return result


# This function allows to insert on the server the observations present in the passed folder,
# if they are not present on the server.
def insert_observations_on_server_from_dir(observations_dir_path, manager_gateway=None):
    result = False

    observations = get_observations_from_dir(observations_dir_path, manager_gateway)

    for observation in observations:
        if observation is not None and isinstance(observation, DefaultEntity):
            result = observation.insert()

    return result


# This function allows to insert on the server an observation and its measurements,
# if they are not present on the server.
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
def insert_observations_and_measurements_on_server(observations, measurements):
    result = None

    if observations is not None and measurements is not None:
        for observation in observations:
            result = insert_observation_and_measurements_on_server(observation, measurements[hash(observation)])

    return result


# This function allows to insert on the server an observation and their measurements
# present in the passed folder, if they are not present on the server.
def insert_observation_and_measurements_on_server_from_dir(observation_dir_path, manager_gateway=None):
    result = None
    observation, measurements = get_observation_and_measurements_from_dir(observation_dir_path, manager_gateway)

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
def insert_observations_and_measurements_on_server_from_dir(observations_dir_path, manager_gateway=None):
    result = None
    observations, measurements = get_observations_and_measurements_from_dir(observations_dir_path, manager_gateway)

    for observation in observations:
        result = insert_observation_and_measurements_on_server(observation, measurements[hash(observation)])

    return result

#endregion