# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# This method returns all the columns and their information of the table Observation.
columns_info = ObservationFunctions.get_info_observation_table_columns(gateways_manager)

# To check if the result is correct we print the method returned.
print(columns_info)
