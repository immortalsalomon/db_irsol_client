

class Measurement:

    def __init__(self):
        self.parameters = dict()
        self.__gateway = default_gateway.DefaultGateway("Measurement")

    def load_measurement_from_id(self, id_measurement):
        self.parameters = self.__gateway.get_by_id(id_measurement)

    def load_measurement_from_data(self, parameters):
        self.parameters = parameters

    def load_measurement_from_dir(self, directory_measurement_path):
        self.parameters = Measurement.get_measurements_from_dir(directory_measurement_path).parameters

    def insert(self, id_observation):
        result = False

        if 'id_measurement' not in self.parameters.keys():
            self.parameters['fk_observation'] = id_observation

            result = self.__gateway.insert(self.parameters)

        return result

    def update(self):
        result = False

        if 'id_measurement' in self.parameters.keys():
            body = copy.deepcopy(self.parameters)
            id_record = body.pop('id_measurement', None)

            result = self.__gateway.update(id_record, body)

        return result

    def delete(self):
        result = False

        if 'id_measurement' in self.parameters.keys():
            result = self.__gateway.delete(self.parameters['id_measurement'])

        return result

    # Utility Methods

    @staticmethod
    def get_measurements_from_dir(directory_measurement_path, only_mmd_file=False):

        measurements_z3bd_files = []
        measurements_fits_files = []
        measurements = []

        for root, directories, files in os.walk(directory_measurement_path):
            for file in files:
                # Path of the measurement
                measurement_file_path = os.path.join(root, file)
                # Check if the measurement contains a ignore keyword in the name
                if not any(substring in file for substring in constant.MEASUREMENTS_IGNORE_KEYS_WORDS):
                    if ".z3bd" in file:
                        if only_mmd_file and "_mmd" in file:
                            measurements_z3bd_files.append(measurement_file_path)
                        elif not only_mmd_file:
                            measurements_z3bd_files.append(measurement_file_path)
                    elif ".fits" in file:
                        measurements_fits_files.append(measurement_file_path)

        for measurement in measurements_z3bd_files:
            measurements.append(Measurement.get_measurement_from_z3bd_file(measurement))

        for measurement in measurements_fits_files:
            measurements.append(Measurement.get_measurement_from_fits_file(measurement))

        return measurements

    @staticmethod
    def get_measurement_from_z3bd_file(measurement_file_path):

        file_path = measurement_file_path
        if ".gz" in measurement_file_path:
            file_path = unzip_file(measurement_file_path)

        measurement = Measurement()
        measurement.parameters = parsers.Parser.parse_measure_z3db_file(file_path)

        measurement.parameters["name"] = os.path.basename(os.path.normpath(file_path.split(".")[0].replace("_mmd", "")))

        if ".gz" in measurement_file_path:
            os.remove(file_path)

        return measurement

    @staticmethod
    def get_measurement_from_fits_file(measurement_file_path):

        file_path = measurement_file_path
        if ".gz" in measurement_file_path:
            file_path = unzip_file(measurement_file_path)

        measurement = Measurement()
        measurement.parameters = parsers.Parser.parse_measure_fits_file(file_path)

        measurement.parameters["name"] = os.path.basename(os.path.normpath(file_path.replace(".fits", "")))

        if ".gz" in measurement_file_path:
            os.remove(file_path)

        return measurement

    @staticmethod
    def get_measurements_from_observation_id(id_observation):
        measurements = []
        measurement_gateway = default_gateway.DefaultGateway("Measurement")
        results = measurement_gateway.get_by_parameters({"fk_observation": id_observation})
        for measurement_parameters in results:
            observation_measurement = Measurement()
            observation_measurement.load_measurement_from_data(measurement_parameters)
            measurements.append(observation_measurement)

        return measurements
