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

# This method returns the number of records inside the Observation table.
number_of_records = ObservationFunctions.get_number_of_records_observation_table(gateways_manager)

# To check if the result is correct we print what the method returned.
print(number_of_records)
