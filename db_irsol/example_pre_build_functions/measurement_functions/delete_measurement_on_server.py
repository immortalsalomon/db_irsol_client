# Import the pre build functions for the gateways.
from db_irsol.pre_build_functions.gateway_functions import GatewayFunctions
# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions
# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# The following line returns a gateway manager. The gateway manager is used to manage all the entry point provided by
# the REST API service.
gateways_manager = GatewayFunctions.get_gateways_manager_with_credentials("username", "password")

# You can specify if you want include in the research the modified and/or the deleted data.
gateways_manager.set_consider_modified_records(False)
gateways_manager.set_consider_deleted_records(False)

# This method returns a set of observations and a dictionary of set of related measurements.
# Both the observations and the measurements are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of the
# observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and its measurements.
observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir("path")

# Add the observation and the measurements into the database. The function returns the id of
# the observation record added into the database.
id_record_observation = ObservationFunctions.insert_observation_and_measurements_on_server(observation, measurements,
                                                                                           gateways_manager)

# To delete a measurement it need to be in the database.
# Delete a measurement in the database. The method returns true if the measurement is delete otherwise return false.
if len(measurements) > 0:
    # This method deletes the measurement in the database.
    result = MeasurementFunctions.delete_measurement_on_server(next(iter(measurements)), gateways_manager)
    # Test if the result is correct we print the result of the method.
    print(result)
