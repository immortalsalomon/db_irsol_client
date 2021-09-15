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

# To update an observation, the observation need to be on the server.
# Define the dictionary that contains as keys the columns you want to modify and as values the new values of
# the columns.
# For this example we will change the rpath of the retrieved observation.
parameters_to_update = {"rpath": "ciaobello"}

# Update a observation in the database. The method returns the new id of the updated observation record
# in the database.
id_record_observation = ObservationFunctions.update_observation_on_server(observation, parameters_to_update,
                                                                          gateways_manager)

# Test if the result is correct we print the id of the modified observation.
print(id_record_observation)
