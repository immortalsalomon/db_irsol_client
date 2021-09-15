# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Measurements entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# You can specify if you want include in the research the modified and/or the deleted data.
gateways_manager.set_consider_modified_records(False)
gateways_manager.set_consider_deleted_records(False)

# This method returns the measurements in the database that match the parameters passed within the range defined
# by the parameters.

# The "<start_element_number>" placeholder is used to define from which record (measurement) start to retriever.
# The "<number_of_elements>" placeholder is used to define how many records (measurements) retriever starting from
# the start_element_number.
# Each time, before searching inside the Measurement table, all the records (measurement) are sorted by id.
# So if the database is not altered this function returns the same results with the same parameters.
# Replace the placeholder "<start_element_number>" and "<number_of_elements>".

# We declare a dictionary that it will contain the parameters and their values.
# The keys of the dictionary need to be the columns names of the Measurement table.
# The value can be anything you want to search.
# In the following example we search all Measurements that name contains a character f.
parameters = {'name': 'f'}

# There is a more complex search that can be done with the parameters and their value,
# but for now it is not documented but it works. For example, if we know the path, or a part of it, of an observation
# in the database. It is possible to add the key "fk_observation-rpath" to the dictionary. The first part
# "fk_observation" tell to the program on which column we desired to do the research. The second part
# "rpath" tell to the program that it first need to search in the Observation table the observation with the same rpath
# as the set value in the dictionary. If an observation record is found it retrieves it's id and search for all the
# measurement with that observation id.
parameters['fk_observation-rpath'] = '/home'

measurements = MeasurementFunctions.get_measurements_chunk_by_parameters_from_server("<start_element_number>",
                                                                                     "<number_of_elements>",
                                                                                     parameters, gateways_manager)

# To check if the result is correct we print what the method returned.
# We print the parameters of the measurement founded.
if measurements is not None:
    for measurement in measurements:
        print(measurement.get_parameters())