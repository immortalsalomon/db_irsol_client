# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions

# The following line return an authenticate gateway object. This object is use to authenticate on the REST API service.
# Need to put yours credentials in place of the username and password placeholder.
authenticate_gateway = GatewayFunctions.get_authenticate_gateway("username", "password")

# The following line is to test if the credentials passed to the previous method are valid.
print(authenticate_gateway.get_token())
