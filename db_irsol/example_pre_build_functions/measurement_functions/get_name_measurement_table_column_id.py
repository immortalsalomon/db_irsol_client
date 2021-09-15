# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# This method returns the name of the column that contains the ids of the measurements.
# The id is a unique unsigned int that identify a record.
column_id = MeasurementFunctions.get_name_measurement_table_column_id(gateways_manager)

# To check if the result is correct we print what the method returned.
print(column_id)
