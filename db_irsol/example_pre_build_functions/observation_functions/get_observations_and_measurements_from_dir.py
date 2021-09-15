# Import the pre build functions for the Observation entry point on the REST API service.
from db_irsol.pre_build_functions.observation_functions import ObservationFunctions

# This method returns a set of observations and a dictionary of set of related measurements.
# Both the observations and the measurements are instances of the DefaultEntity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the
# path of the folder that contains all the observations. Like "/home/mushu/Desktop/irsol/data/irsol_old/2017" is a
# folder that contains all the observations from 2017.
observations, measurements = ObservationFunctions.get_observations_and_measurements_from_dir("path")

# To check if the result is correct we print what the method returned.
# We print the parameters of the observations and of the measurements founded.
if observations is not None:
    # We do a loop over the set of observations and we print their parameters and measurements.
    for observation in observations:
        # Print observation parameters
        print(observation.get_parameters())

        # The keys of the dictionary are the hash of the observations object.
        for measurement in measurements[hash(observation)]:
            # Print measurement parameters
            print(measurement.get_parameters())

        print("------------------------------")
