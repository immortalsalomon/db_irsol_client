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
# You need to pass a valid path to the following method. Replace the placeholder <path> with the path of the
# observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and its measurements.
observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir("path")

# Add the observation into the database. The function returns the id of the observation record added into the database.
id_record_observation = ObservationFunctions.insert_observation_on_server(observation, gateways_manager)

# To all the measurements found we add the field (column) fk_observation. The value of the field is the id of
# the observation added in the previous line.
for measurement in measurements:
    measurement.add_parameters({"fk_observation": id_record_observation})

# This method adds the measurement into the database. It returns a dictionary where the keys are the hash of
# the measurements objects and the values are the ids of the added measurements records in the database.
ids_records_measurements = MeasurementFunctions.insert_measurements_on_server(measurements, gateways_manager)

# Test if the result is correct we print the ids of the measurements records in the database.
if ids_records_measurements is not None:
    for key, value in ids_records_measurements.items():
        print(str(key) + " => " + str(value))
