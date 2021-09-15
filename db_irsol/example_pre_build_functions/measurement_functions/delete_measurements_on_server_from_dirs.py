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

# Add an observation and the measurements to the database. The function returns the id of the observation record in the
# database.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and it's measurements.
id_record_observation = ObservationFunctions.insert_observation_and_measurements_on_server_from_dir("path",
                                                                                                    gateways_manager)

# Add an observation and the measurements to the database. The function returns the id of the observation record in the
# database.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and it's measurements.
id_record_observation = ObservationFunctions.insert_observation_and_measurements_on_server_from_dir("path",
                                                                                                    gateways_manager)

# This method deletes the measurements in the database. It return a dictionary where the keys are the hash of the
# measurements objects and the values are boolean. True if the measurement is deleted otherwise False.
# It returns False also if the measurement is already deleted.
# You need to pass some valid paths to the following method. Replace the placeholders path with the
# paths of folders that contain some measurements. Like "/home/mushu/Desktop/irsol/data/irsol_old/2018/181023/raw" is a
# folder that contains some measurements from 2018.
# It returns a dictionary where the keys are the hash of the measurements objects and the values are the ids of
# the added measurements records in the database.
results = MeasurementFunctions.delete_measurements_on_server_from_dirs(["path", "path"], gateways_manager)

# To check if the result is correct we print the result of the previous method.
for key, value in results.items():
    print(str(key) + " => " + str(value))
