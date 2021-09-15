# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# You can specify if you want include in the research the modified and/or the deleted data.
gateways_manager.set_consider_modified_records(False)
gateways_manager.set_consider_deleted_records(False)

# This method returns a set of observations .
# The observations are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the
# path of the folder that contains all the observations. Like "/home/mushu/Desktop/irsol/data/irsol_old/2017" is a
# folder that contains all the observations from 2017.
observation = ObservationFunctions.get_observation_from_dir("path")

# Add the observation into the database. The function returns the id of the observation record added into the database.
id_record_observation = ObservationFunctions.insert_observation_on_server(observation, gateways_manager)

# To check if the result is correct we print the id of the added observation.
print(id_record_observation)
