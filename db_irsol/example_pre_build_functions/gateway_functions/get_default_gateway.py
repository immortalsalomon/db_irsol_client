# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions

# The following line return a default gateway for the Observations.
# The dafault_gateway allow to communicate with the service REST API on a specific entry point.
default_gateway = GatewayFunctions.get_default_gateway("Observation.php")
