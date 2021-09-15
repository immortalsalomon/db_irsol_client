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

# To update some observations, the observations need to be in the database.
# Define the dictionary that contains one dictionary for each observation to modify. The keys of the primary dictionary
# are the hash of the observations objects. The values are other dictionaries that contain as keys the columns you want
# to modify and as values the new values of the columns.
# For this example wi will modify the weather_condition column of al the observations given by the previous method.
# In this case we set the weather_conditions equal for all because is a faster example.
parameters_to_update = {}
if observations is not None:
    for observation in observations:
        parameters = {"weather_condition": "funny"}
        parameters_to_update[hash(observation)] = parameters

# Update some observations in the database. The method returns the new ids of the updated observations records
# in the database.
ids_records_observations = ObservationFunctions.update_observations_on_server(observations, parameters_to_update,
                                                                              gateways_manager)

# Test if the result is correct we print the ids of the updated observations records.
print(ids_records_observations)
