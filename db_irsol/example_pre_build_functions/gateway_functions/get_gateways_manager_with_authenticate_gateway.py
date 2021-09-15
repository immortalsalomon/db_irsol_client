# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions

# The following line return an authenticate gateway object. This object is use to authenticate on the REST API service.
# Need to put yours credentials in place of the username and password placeholder.
authenticate_gateway = GatewayFunctions.get_authenticate_gateway("username", "password")

# The following line return a gateway manager. The gateway manager is used to manage all the entry point provided by
# the service REST API.
gateways_manager = GatewayFunctions.get_gateways_manager_with_authenticate_gateway(authenticate_gateway)
