# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions

# The following line return a gateway manager. The gateway manager is used to manage all the entry point provided by
# the service REST API.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")
