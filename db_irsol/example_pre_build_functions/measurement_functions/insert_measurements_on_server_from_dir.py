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

# This method returns an object that represent an observation. The object is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation.
observation = ObservationFunctions.get_observation_from_dir("path")

# Add the observation into the database. The method return the id of the observation record in the database.
id_record_observation = ObservationFunctions.insert_observation_on_server(observation, gateways_manager)

# The following method inserts some measurements from a measurement folder. Replace the placeholder path with the path
# of the measurements folder, like "home/mushu/Desktop/git_irsol/2018/181023/raw".
# It returns a dictionary where the key are the hash of the measurement object and the value is the id of the added
# measurement record in the database.
ids_records_measurements = MeasurementFunctions.insert_measurements_on_server_from_dir("path", id_record_observation,
                                                                                       gateways_manager)

# Test if the observation is added.
if ids_records_measurements is not None:
    for key, value in ids_records_measurements.items():
        print(str(key) + " => " + str(value))
