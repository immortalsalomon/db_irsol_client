# Import the pre build functions for the Measurement entry point on the REST API service.
from db_irsol.pre_build_functions.measurement_functions import MeasurementFunctions

# This method returns a measurement. The measurement is an instance of the Default Entity class.
# You need to pass a valid path to the following method. Replace the placeholder path with the path of the measurement
# file, like = "/home/mushu/Desktop/git_irsol/2018/181023/raw/caln5140m1.z3bd".
measurement = MeasurementFunctions.get_measurement_from_file("path")

# To check if the result is correct we print what the method returned.
# We print the parameters of the measurement
if measurement is not None:
    print(measurement.get_parameters())
