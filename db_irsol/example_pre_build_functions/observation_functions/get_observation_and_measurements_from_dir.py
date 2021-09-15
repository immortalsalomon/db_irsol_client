# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# This method returns one observation and a set of related measurements. Both the observation and the measurements
# are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder <path> with the path of the
# observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation and its measurements.
observation, measurements = ObservationFunctions.get_observation_and_measurements_from_dir("<path>")

# To check if the result is correct we print what the method returned.
# We print the parameters of the observation and of the measurements founded.
if observation is not None:
    print(observation.get_parameters())

if measurements is not None:
    for measurement in measurements:
        print(measurement.get_parameters())
