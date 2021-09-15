from db_irsol.api_gateway.gateway_manager import GatewayManager
from db_irsol.entities.entities.default_entity import DefaultEntity
from db_irsol.entities.utility import unzip_file
from db_irsol.parsers.measurement_parser import MeasurementParser
from db_irsol.parsers.log_parser import LogParser
from db_irsol.settings import Settings


from multiprocessing import Pool, cpu_count
import os
import re
import copy
import tempfile


class EntityManager:

    def __init__(self, gateway_manager=None):
        self.__gateway_manager = None
        self.__table_columns_names = {}
        self.__table_not_null_columns_names = {}
        self.__table_column_id_name = {}
        self.__table_columns_needed = {}
        self.__table_unique_identifier_columns = {}
        self.set_gateway_manager(gateway_manager)

    def set_gateway_manager(self, gateway_manager):
        to_return = False

        if gateway_manager is None:
            print("The passed gateway_manager is None. Please provide a valid one.")
        elif not isinstance(gateway_manager, GatewayManager):
            print("The passed gateway_manager is not an instance of the class GatewayManager.")
        elif not gateway_manager.get_is_authentication_working():
            print("The passed gateway_manager can not authenticate on the REST API service.")
        else:
            self.__gateway_manager = gateway_manager
            authenticate_gateway = gateway_manager.get_authenticate_gateway()

            for key, default_gateway in gateway_manager.get_default_gateways().items():

                columns_names = default_gateway.get_table_columns_names(authenticate_gateway)
                if columns_names is not None:
                    self.__table_columns_names[default_gateway.get_entry_point()] = columns_names

                not_null_columns_names = default_gateway.get_table_not_null_columns_names(authenticate_gateway)
                if not_null_columns_names is not None:
                    self.__table_not_null_columns_names[default_gateway.get_entry_point()] = not_null_columns_names

                column_id = default_gateway.get_table_column_id_name(authenticate_gateway)
                if column_id is not None:
                    self.__table_column_id_name[default_gateway.get_entry_point()] = column_id

                if column_id is not None and not_null_columns_names is not None:
                    self.__table_columns_needed[default_gateway.get_entry_point()] = not_null_columns_names
                    self.__table_columns_needed[default_gateway.get_entry_point()].remove(column_id)

                unique_identifier_columns = default_gateway.get_unique_identifier_columns(authenticate_gateway)
                if unique_identifier_columns is not None:
                    self.__table_unique_identifier_columns[default_gateway.get_entry_point()] =\
                        unique_identifier_columns

            to_return = True

        return to_return

    def insert(self, default_entity):
        to_return = None

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif default_entity is None:
            print("The method's parameter is None.")
        elif not isinstance(default_entity, DefaultEntity):
            print("The passed parameter is not an instance of DefaultEntity.")
        elif default_entity.is_entity_synchronized_with_server():
            print("The DefaultEntity is already present on the server.")
        elif all(any(needed_columns in parameter for parameter in default_entity.get_parameters().keys())
                 for needed_columns
                 in self.__table_columns_needed[default_entity.get_entry_point()]):

            entity_gateway = self.__gateway_manager.get_default_gateway(default_entity.get_entry_point())
            to_return = entity_gateway.insert(default_entity.get_parameters(),
                                              self.__gateway_manager.get_authenticate_gateway())

            if to_return is not None:
                self.synchronize_entity_with_server(default_entity)

        else:
            print("Not all fields(column) needed are present in the parameters of the entity.")

        return to_return

    def update(self, default_entity, parameters_to_update={}):
        to_return = False

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif default_entity is None or parameters_to_update is None:
            print("One or both method's parameters are None.")
        elif not isinstance(default_entity, DefaultEntity):
            print("The passed parameter is not an instance of DefaultEntity.")
        elif not default_entity.is_entity_synchronized_with_server():
            print("Can't update an entity that is not synchronized with the server. Please synchronize the entity.")
        else:

            new_entity_parameters = {**default_entity.get_parameters(), **parameters_to_update}

            if all(any(needed_columns in parameter for parameter in default_entity.get_parameters().keys())
                   for needed_columns
                   in self.__table_columns_needed[default_entity.get_entry_point()]):

                entity_gateway = self.__gateway_manager.get_default_gateway(default_entity.get_entry_point())
                id_entity = \
                    default_entity.get_parameters()[self.__table_column_id_name[default_entity.get_entry_point()]]
                to_return = entity_gateway.update(id_entity, new_entity_parameters,
                                                  self.__gateway_manager.get_authenticate_gateway())

                if to_return is not None:
                    self.synchronize_entity_with_server(default_entity)

            else:
                print("Not all fields(column) needed are present in the parameters of the entity.")

        return to_return

    def delete(self, default_entity):
        to_return = False

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif default_entity is None:
            print("The method's parameter is None.")
        elif not isinstance(default_entity, DefaultEntity):
            print("The passed parameter is not an instance of DefaultEntity.")
        elif not default_entity.is_entity_synchronized_with_server():
            print("Can't delete an entity that is not synchronized with the server. Please synchronize the entity.")
        else:

            entity_gateway = self.__gateway_manager.get_default_gateway(default_entity.get_entry_point())
            id_entity = \
                default_entity.get_parameters()[self.__table_column_id_name[default_entity.get_entry_point()]]
            to_return = entity_gateway.delete(id_entity, self.__gateway_manager.get_authenticate_gateway())

            if to_return is not None:
                self.synchronize_entity_with_server(default_entity)

        return to_return

    def get_entity_by_id_from_server(self, id_entity, entry_point):
        to_return = None

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif id_entity is None or entry_point is None:
            print("One or both method's parameters are None.")
        else:
            default_gateway = self.__gateway_manager.get_default_gateway(entry_point)
            if default_gateway is None:
                print("There is not a default gateway for the entry point passed in the gateway manager.")
            else:
                entity = default_gateway.get_by_id(id_entity, self.__gateway_manager.get_authenticate_gateway())
                if entity is not None and len(entity) > 0:
                    to_return = DefaultEntity(entry_point)
                    to_return.set_parameters(entity[0], True)
                else:
                    print("Can't retrieve the entity from the server.")

        return to_return

    def get_entities_chunk_from_server(self, start_element_number, number_of_elements, entry_point):
        to_return = None

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif start_element_number is None or entry_point is None or number_of_elements is None:
            print("One or all method's parameters are None.")
        else:
            default_gateway = self.__gateway_manager.get_default_gateway(entry_point)
            if default_gateway is None:
                print("There is not a default gateway for the entry point passed in the gateway manager.")
            else:
                entities = default_gateway.get_chunk(start_element_number, number_of_elements,
                                                     self.__gateway_manager.get_authenticate_gateway())
                if entities is not None:
                    to_return = set()
                    for entity in entities:
                        current_entity = DefaultEntity(entry_point)
                        current_entity.set_parameters(entity, True)
                        to_return.add(current_entity)
                else:
                    print("Can't retrieve the entity/entities from the server.")

        return to_return

    def get_entities_by_parameters_from_server(self, parameters, entry_point):
        to_return = None

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif parameters is None or entry_point is None:
            print("One or both method's parameters are None.")
        else:
            default_gateway = self.__gateway_manager.get_default_gateway(entry_point)
            if default_gateway is None:
                print("There is not a default gateway for the entry point passed in the gateway manager.")
            else:
                entities = default_gateway.get_by_parameters(parameters,
                                                             self.__gateway_manager.get_authenticate_gateway())
                if entities is not None:
                    to_return = set()
                    for entity in entities:
                        current_entity = DefaultEntity(entry_point)
                        current_entity.set_parameters(entity, True)
                        to_return.add(current_entity)
                else:
                    print("Can't retrieve the entity/entities from the server.")

        return to_return

    def get_entities_chunk_by_parameters_from_server(self, start_element_number, number_of_elements, parameters,
                                                     entry_point):
        to_return = None

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif start_element_number is None or entry_point is None or number_of_elements is None and parameters is None:
            print("One or all method's parameters are None.")
        else:
            default_gateway = self.__gateway_manager.get_default_gateway(entry_point)
            if default_gateway is None:
                print("There is not a default gateway for the entry point passed in the gateway manager.")
            else:
                entities = default_gateway.get_chunk_by_parameters(start_element_number, number_of_elements, parameters,
                                                                   self.__gateway_manager.get_authenticate_gateway())
                if entities is not None and len(entities) > 0:
                    to_return = set()
                    for entity in entities:
                        current_entity = DefaultEntity(entry_point)
                        current_entity.set_parameters(entity, True)
                        to_return.add(current_entity)
                else:
                    print("Can't retrieve the entity/entities from the server.")

        return to_return

    def synchronize_entity_with_server(self, default_entity):
        to_return = False

        if self.__gateway_manager is None:
            print("The gateway_manager is None. Please provide a valid one.")
        elif default_entity is None:
            print("The method parameter is None.")
        elif not isinstance(default_entity, DefaultEntity):
            print("The passed parameter is not an instance of DefaultEntity.")
        else:

            entity_parameters = default_entity.get_parameters()
            id_column_entry_point = self.__table_column_id_name[default_entity.get_entry_point()]
            server_entity = None

            if id_column_entry_point in entity_parameters.keys():
                server_entity = self.__gateway_manager.get_default_gateway(default_entity.get_entry_point())\
                    .get_by_id(entity_parameters[id_column_entry_point],
                               self.__gateway_manager.get_authenticate_gateway())
            else:
                unique_identifier_parameters = {}
                unique_identifier_columns = copy.deepcopy(
                    self.__table_unique_identifier_columns[default_entity.get_entry_point()])
                for key, value in entity_parameters.items():

                    if key in unique_identifier_columns:
                        unique_identifier_parameters[key] = value
                        unique_identifier_columns.remove(key)
                        continue

                    for column in unique_identifier_columns:
                        if column in key:
                            unique_identifier_parameters[key] = value
                            unique_identifier_columns.remove(column)
                            continue

                server_entity = self.__gateway_manager.get_default_gateway(default_entity.get_entry_point()) \
                    .get_by_parameters(unique_identifier_parameters, self.__gateway_manager.get_authenticate_gateway())

            if server_entity is not None:
                if len(server_entity) > 1:
                    print("Found more then one possible entity on the server. Impossible to know on what synchronize.")
                elif len(server_entity) == 0:
                    print("The program was not able to find the passed entity in the database."
                          " Are you sure that the entity is in the database")
                else:
                    default_entity.clear_parameters()
                    default_entity.set_parameters(server_entity[0], True)
                    to_return = True
            else:
                print("Can't retrieve the entity/entities from the server.")

        return to_return

    def synchronize_entities_with_server(self, default_entities):
        to_return = {}

        for default_entity in default_entities:
            to_return[hash(default_entity)] = self.synchronize_entity_with_server(default_entity)

        return to_return

    @staticmethod
    def get_measurement_from_z3bd_file(measurement_file_path):

        file_path = measurement_file_path

        with tempfile.TemporaryDirectory() as tmpdirname:
            if ".gz" in measurement_file_path:
                file_path = unzip_file(measurement_file_path, tmpdirname)

            parameters = MeasurementParser.parse_z3db_file(file_path)
            parameters["name"] = os.path.basename(os.path.normpath(measurement_file_path))

            measurement = DefaultEntity("Measurement.php")
            measurement.set_parameters(parameters)

        return measurement

    @staticmethod
    def get_measurement_from_fits_file(measurement_file_path):

        file_path = measurement_file_path
        with tempfile.TemporaryDirectory() as tmpdirname:
            if ".gz" in measurement_file_path:
                file_path = unzip_file(measurement_file_path, tmpdirname)

            parameters = MeasurementParser.parse_fits_file(file_path)
            parameters["name"] = os.path.basename(os.path.normpath(measurement_file_path))

            measurement = DefaultEntity("Measurement.php")
            measurement.set_parameters(parameters)

        return measurement

    @staticmethod
    def get_measurements_from_dir(directory_measurement_path, only_mmd_file=False):

        measurements_z3bd_files = []
        measurements_fits_files = []
        measurements = set()

        for root, directories, files in os.walk(directory_measurement_path):
            for file in files:
                # Path of the measurement
                measurement_file_path = os.path.join(root, file)
                # Check if the measurement contains a ignore keyword in the name
                if not any(substring in file for substring in Settings.keywords_to_ignore_measurements):
                    if ".z3bd" in file:
                        if only_mmd_file and "_mmd" in file:
                            measurements_z3bd_files.append(measurement_file_path)
                        elif not only_mmd_file:
                            measurements_z3bd_files.append(measurement_file_path)
                    elif ".fits" in file:
                        measurements_fits_files.append(measurement_file_path)

        pool = Pool(cpu_count())

        for measurement in measurements_z3bd_files:
            pool.apply_async(EntityManager.get_measurement_from_z3bd_file, (measurement,),
                             callback=measurements.add)

        for measurement in measurements_fits_files:
            pool.apply_async(EntityManager.get_measurement_from_fits_file, (measurement,),
                             callback=measurements.add)

        pool.close()
        pool.join()

        return measurements

    @staticmethod
    def get_observation_and_measurements_from_dir(directory_observation_path):

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

        measurements = EntityManager.get_measurements_from_dir(measurement_dir, only_mmd_file)

        observation = None

        # Get telescope name if not in log file
        if "fk_telescope-name" not in parameters.keys():
            for measurement in measurements:
                if "fk_telescope-name" in measurement.get_parameters():
                    parameters["fk_telescope-name"] = measurement.get_parameters()["fk_telescope-name"]
                    break

        if "fk_telescope-name" in parameters.keys():
            observation = DefaultEntity('Observation.php')
            observation.set_parameters(parameters)

        return observation, measurements
