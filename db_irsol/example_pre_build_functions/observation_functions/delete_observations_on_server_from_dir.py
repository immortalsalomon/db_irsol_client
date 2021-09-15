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

# To delete an observation the observation need to be in the database.
# Delete some observations in the database. The method returns a dictionary. The keys are the hash of the observations
# objects, while the values are a boolean. True if an observation is deleted and false otherwise. False is returned
# also if the observation is already deleted.
# You need to pass a valid path to the following method. Replace the placeholder path with the
# path of the folder that contains all the observations. Like "/home/mushu/Desktop/irsol/data/irsol_old/2017" is a
# folder that contains all the observations from 2017.
result = ObservationFunctions.delete_observations_on_server_from_dir("path", gateways_manager)

# Test if the result is correct we print the result of the method.
print(result)
