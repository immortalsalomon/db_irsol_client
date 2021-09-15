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

# This method returns an object that represent an observation. The object is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation.
observation = ObservationFunctions.get_observation_from_dir("path")

# To delete an observation the observation need to be in the database.
# Delete an observation in the database. The method returns true if the observation is delete otherwise return false.
# False is returned also if the observation is already deleted.
result = ObservationFunctions.delete_observation_on_server(observation, gateways_manager)

# Test if the result is correct we print the return of the previous method.
print(result)
