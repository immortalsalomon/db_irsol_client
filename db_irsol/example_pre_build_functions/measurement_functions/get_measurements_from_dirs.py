# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# This method returns a set of measurements. The measurements are instance of the Default Entity class.
# You need to pass some valid paths to the following method. Replace the placeholders path with the
# paths of folders that contain some measurements. Like "/home/mushu/Desktop/irsol/data/irsol_old/2018/181023/raw" is a
# folder that contains some measurements from 2018.
measurements = MeasurementFunctions.get_measurements_from_dirs(["path", "path"])

# To check if the result is correct we print what the method returned.
# We print the parameters of the measurements founded.
if measurements is not None:
    # We do a loop over the set of measurements and we print their parameters.
    for measurement in measurements:
        print(measurement.get_parameters())
