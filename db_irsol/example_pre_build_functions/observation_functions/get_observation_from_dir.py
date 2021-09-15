# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# This method returns an object that represent an observation. The object is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of
# the observation folder, like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226".
# The folder 170226 contains an observation.
observation = ObservationFunctions.get_observation_from_dir("path")

# To check if the result is correct we print what the method returned.
# We print the parameters of the observation founded.
if observation is not None:
    print(observation.get_parameters())
