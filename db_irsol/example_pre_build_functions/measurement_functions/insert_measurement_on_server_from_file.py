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

# Add an observation into the database. The function returns the id of the observation record in the database.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/git_irsol/2018/181023".
# The folder 170226 contains an observation.
id_record_observation = ObservationFunctions.insert_observation_on_server_from_dir("path", gateways_manager)

# Add a measurement into the database. The measurement is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of the measurement
# file, like = "/home/mushu/Desktop/git_irsol/2018/181023/raw/caln5140m1.z3bd".
id_record_measurement = MeasurementFunctions.insert_measurement_on_server_from_file("path", id_record_observation,
                                                                                    gateways_manager)

# To check if the result is correct we print the id of the added measurement.
print(id_record_measurement)
