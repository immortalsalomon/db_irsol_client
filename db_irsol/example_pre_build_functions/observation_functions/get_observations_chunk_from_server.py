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

# This method returns the observations in the database within the range defined by the parameters.
# The "<start_element_number>" placeholder is used to define from which record (observation) start to retriever.
# The "<number_of_elements>" placeholder is used to define how many records (observations) retriever starting from
# the start_element_number.
# Each time, before searching inside the Observation table, all the records (observations) are sorted by id.
# So if the database is not altered this function returns the same results with the same parameters.
# Replace the placeholder "<start_element_number>" and "<number_of_elements>".
observations = ObservationFunctions.get_observations_chunk_from_server("<start_element_number>",
                                                                       "<number_of_elements>", gateways_manager)

# To check if the result is correct we print what the method returned.
# We print the parameters of the observations retrieved.
if observations is not None:
    for observation in observations:
        print(observation.get_parameters())
