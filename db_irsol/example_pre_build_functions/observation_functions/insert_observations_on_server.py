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

# This method returns a set of observations .
# The observations are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the
# path of the folder that contains all the observations. Like "/home/mushu/Desktop/irsol/data/irsol_old/2017" is a
# folder that contains all the observations from 2017.
observations = ObservationFunctions.get_observations_from_dir("path")

# Add some observations into the database. The method returns a dictionary. The keys are the hash of the observations
# objects, while the values are the ids of the added observations records in the database.
ids_records_observations = ObservationFunctions.insert_observations_on_server(observations, gateways_manager)

# Test if the result is correct we print the ids of the added observations records.
if ids_records_observations is not None:
    print(ids_records_observations)
