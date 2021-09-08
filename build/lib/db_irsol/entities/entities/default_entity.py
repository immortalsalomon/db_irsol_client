

class DefaultEntity:

    def __init__(self, entry_point=None):
        self.__entry_point = entry_point
        self.__parameters = {}
        self.__parameters_synchronization_flags = {}

    def get_entry_point(self):
        return self.__entry_point

    def get_parameters(self):
        return self.__parameters

    def get_parameters_synchronization_flags(self):
        return self.__parameters_synchronization_flags

    def is_entity_synchronized_with_server(self):
        to_return = False

        if len(self.__parameters_synchronization_flags) > 0 \
            and all(value == 1 for value in self.__parameters_synchronization_flags.values()) \
                and set(self.__parameters.keys()) == set(self.__parameters_synchronization_flags.keys()):
            to_return = True

        return to_return

    def __eq__(self, other):
        to_return = False

        other_parameters = other.get_parameters()

        if self.__class__ != other.__class__:
            to_return = False
        elif other_parameters is None and self.__parameters is None:
            to_return = True
        elif other_parameters is None or self.__parameters is None:
            to_return = False
        else:
            if set(self.__parameters.keys()) == set(other_parameters.keys()):
                if all(self.__parameters[parameter] == other_parameters[parameter]
                       for parameter in self.__parameters.keys()):
                    to_return = True
            else:
                to_return = False

        return to_return

    def __hash__(self):
        string_to_hash = ""

        for key, value in self.__parameters.items():
            string_to_hash += str(value)

        return hash(string_to_hash)

    def set_parameters(self, parameters={}, are_server_parameter=False):

        if parameters is not None:

            self.__parameters = parameters

            if are_server_parameter:
                for key in self.__parameters.keys():
                    self.__parameters_synchronization_flags[key] = 1
            else:
                self.__parameters_synchronization_flags = {}

    def add_parameters(self, parameters={}):

        if parameters is not None:

            parameters_keys = self.__parameters.keys()

            for key, value in parameters.items():
                if key in parameters_keys and key in self.__parameters_synchronization_flags \
                        and self.__parameters[key] != parameters[key]:
                    self.__parameters_synchronization_flags[key] = 0

            self.__parameters = {**self.__parameters, **parameters}

    def remove_parameters(self, parameters=[]):

        if parameters is not None:
            parameters_keys = self.__parameters.keys()
            parameters_synchronization_flags_keys = self.__parameters_synchronization_flags.keys()

            for to_remove_parameter in parameters:
                if to_remove_parameter in parameters_keys:
                    del self.__parameters[to_remove_parameter]

                if to_remove_parameter in parameters_synchronization_flags_keys:
                    self.__parameters_synchronization_flags[to_remove_parameter] = 0

    def clear_parameters(self):

        self.__parameters = {}
        self.__parameters_synchronization_flags = {}
