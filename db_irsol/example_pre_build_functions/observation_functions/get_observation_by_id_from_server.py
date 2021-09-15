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

# This method returns a measurement in the database with the same id passed to it.
# Replace the placeholder "<id>" with the id of a measurement.
observation = ObservationFunctions.get_observation_by_id_from_server("<id>", gateways_manager)

# To check if the result is correct we print what the method returned.
# We print the parameters of the observation retrieved.
if observation is not None:
    print(observation.get_parameters())
