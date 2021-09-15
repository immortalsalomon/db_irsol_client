# Import external library to make a deep copy of an object.
import copy

# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions
# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# You can specify if you want include in the research the modified and/or the deleted data.
gateways_manager.set_consider_modified_records(False)
gateways_manager.set_consider_deleted_records(False)

# This method returns one observation and a set of related measurements. Both the observation and the measurements
# are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of the
# observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and its measurements.
observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir("path")

# Add the observation and the measurements into the database. The function returns the id of
# the observation record added into the database.
id_record_observation = ObservationFunctions.insert_observation_and_measurements_on_server(observation,
                                                                                           measurements,
                                                                                           gateways_manager)

# This dictionary will contain all the new value for the column of all the measurement to update. The keys are
# the hash of the measurements objects and the values are dictionaries containing the parameters to update.
parameters_to_updates = dict()

# Add to measurements some fields (columns) and their values. In this example we change the value of the pigi column.
# Because the fk_observation is part of the unique identifier we need to add the field (column) to the parameters of
# a measurement to allow the program to find the record in the database.
for measurement in measurements:
    measurement.add_parameters({"pigi": 100, "fk_observation": id_record_observation})
    # We make a deep copy of the new parameters of each measurement and we save the parameters inside the dictionary.
    # We do this because before update the program synchronize the measurements with the server and all modified
    # or added parameters are deleted.
    parameters_to_updates[hash(measurement)] = copy.deepcopy(measurement.get_parameters())

# This method update some measurements in the database. The method returns a dictionary where the keys are the hash
# of the measurements objects and the values are the ids of the new measurements records added
# to update the old measurements.
results = MeasurementFunctions.update_measurements_on_server(measurements,
                                                             parameters_to_updates,
                                                             gateways_manager)

if results is not None:
    # To check if the result is correct we print the ids of the new measurements returned by the previous method.
    for key, value in results.items():
        print(str(key) + " => " + str(value))
