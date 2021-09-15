# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# This method returns all the columns names of the table Measurement.
columns_names = MeasurementFunctions.get_names_measurement_table_columns(gateways_manager)

# To check if the result is correct we print what the method returned.
print(columns_names)
