# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# This method returns a set of observations .
# The observations are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the
# path of the folder that contains all the observations. Like "/home/mushu/Desktop/irsol/data/irsol_old/2017" is a
# folder that contains all the observations from 2017.
observations = ObservationFunctions.get_observations_from_dir("path")

# To check if the result is correct we print what the method returned.
# We print the parameters of the observations founded.
if observations is not None:
    # We do a loop over the set of observations and we print their parameters.
    for observation in observations:
        print(observation.get_parameters())
