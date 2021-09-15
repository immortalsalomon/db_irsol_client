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

# This method returns the observations in the database that match the parameters passed.
# We declare a dictionary that it will contain the parameters and their values.
# The keys of the dictionary need to be the columns names of the Observation table.
# The value can be anything you want to search.
# In the following example we search all observations that path start with /home*.
parameters = {'rpath': '/home'}

# There is a more complex search that can be done with the parameters and their value,
# but for now it is not documented but it works. For example, if we know the name, or a part of it, of a telescope
# in the database. It is possible to add the key "fk_telescope-name" to the dictionary. The first part "fk_telescope"
# tell to the program on which column we desired to do the research. The second part "name" tell to the program that
# it first need to search in the Telescope table the telescope with the same name as the set value in the dictionary.
# If a telescope record is found it retrieves  it's id and search for all the observation with that telescope id.
parameters['fk_telescope-name'] = 'GRE'

observations = ObservationFunctions.get_observations_by_parameters_from_server(parameters, gateways_manager)

# To check if the result is correct we print what the method returned.
# We print the parameters of the observations founded.
if observations is not None:
    for observation in observations:
        print(observation.get_parameters())
