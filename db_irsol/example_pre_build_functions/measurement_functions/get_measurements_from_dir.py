# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# This method returns an object that represent the observation. The object is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of the observation.
# A observation path is the path that reach the observation folder,
# like = "/home/mushu/Desktop/irsol/data/irsol_old/2017/170226". The folder 170226 contains an observation.
measurements = MeasurementFunctions.get_measurements_from_dir("path")

# To check if the result is correct we print what the method returned.
# We print the parameters of the measurements founded.
if measurements is not None:
    # We do a loop over the set of measurements and we print their parameters.
    for measurement in measurements:
        print(measurement.get_parameters())
