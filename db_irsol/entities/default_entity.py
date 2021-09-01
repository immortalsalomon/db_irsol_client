

class DefaultEntity:
    table_columns_names = {}
    table_not_null_columns_names = {}

    def __init__(self, default_gateway=None):
        self.__parameters = {}
        self.__default_gateway = default_gateway
        self.__is_synchronized_with_server = False

        if default_gateway is not None:
            columns_names = default_gateway.get_table_columns_names()
            if columns_names is not None and default_gateway.get_entry_point() not in DefaultEntity.table_columns_names:
                DefaultEntity.table_columns_names[default_gateway.get_entry_point()] = columns_names
                DefaultEntity.table_columns_names[default_gateway.get_entry_point()]\
                    .remove(self.__default_gateway.get_table_column_id_name())

            not_null_columns_names = default_gateway.get_table_not_null_columns_names()
            if not_null_columns_names is not None\
                    and default_gateway.get_entry_point() not in DefaultEntity.table_not_null_columns_names:
                DefaultEntity.table_not_null_columns_names[default_gateway.get_entry_point()] = not_null_columns_names
                DefaultEntity.table_not_null_columns_names[default_gateway.get_entry_point()]\
                    .remove(self.__default_gateway.get_table_column_id_name())

    # Get methods

    def get_parameters(self):
        return self.__parameters

    def get_default_gateway(self):
        return self.__default_gateway

    def get_is_synchronized_with_server(self):
        return self.__is_synchronized_with_server

    # Set Methods

    def set_default_gateway(self, default_gateway):
        self.__default_gateway = default_gateway

    # Override methods

    def __eq__(self, other):

        other_parameters = other.get_parameters()
        other_default_gateway = other.get_default_gateway()

        if other_parameters is None and self.__parameters is None:
            return True
        elif other_parameters is None or self.__parameters is None:
            return False
        elif other_default_gateway is not None and self.__default_gateway is not None:

            self_columns_names = DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()]
            other_columns_names = DefaultEntity.table_not_null_columns_names[other_default_gateway.get_entry_point()]

            if set(self_columns_names.keys()) == set(other_columns_names.keys()):
                if all(parameter in self.__parameters.keys() for parameter in self_columns_names) \
                        and all(parameter in other_parameters.keys() for parameter in self_columns_names) \
                        and all(self.__parameters[parameter] == other_parameters[parameter]
                                for parameter in self_columns_names):
                    return True
            else:
                return False
        else:
            if set(self.__parameters.keys()) == set(other_parameters.keys()):
                if all(self.__parameters[parameter] == other_parameters[parameter]
                       for parameter in self.__parameters.keys()):
                    return True
            else:
                return False

    def __hash__(self):
        string_to_hash = ""

        if self.__default_gateway is not None:
            if all(parameter in self.__parameters.keys() for parameter
                   in DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()]):

                for parameter in DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()]:
                    string_to_hash += str(self.__parameters[parameter])

        if string_to_hash == "":
            for key, value in self.__parameters.items():
                string_to_hash += str(value)

        return hash(string_to_hash)

    # Parameter methods

    def add_parameters(self, parameters={}):
        if parameters is not None:
            if not self.__is_synchronized_with_server:
                self.__parameters = {**self.__parameters, **parameters}
                if self.__default_gateway is not None:
                    self.synchronize_parameters_by_parameters()
            else:
                for key, value in parameters.items():
                    if key in DefaultEntity.table_columns_names[self.__default_gateway.get_entry_point()]:
                        self.__is_synchronized_with_server = False

                self.__parameters = {**self.__parameters, **parameters}

    def remove_parameters(self, parameters=[]):

        if parameters is not None:
            parameters_keys = self.__parameters.keys()

            for to_remove_parameter in parameters:
                if to_remove_parameter in parameters_keys:
                    del self.__parameters[to_remove_parameter]

            if self.__is_synchronized_with_server \
                    and all(parameter in self.__parameters.keys()
                            for parameter in
                            DefaultEntity.table_columns_names[self.__default_gateway.get_entry_point()]):
                self.__is_synchronized_with_server = True
            else:
                self.__is_synchronized_with_server = False

    def set_parameters(self, parameters={}, are_server_parameter=False):

        if parameters is not None:

            self.__parameters = parameters

            if self.__default_gateway is not None:
                if are_server_parameter\
                        and all(column_name in parameters.keys()
                                for column_name
                                in DefaultEntity.table_columns_names[self.__default_gateway.get_entry_point()]):
                    self.__is_synchronized_with_server = True
                else:
                    self.synchronize_parameters_by_parameters()

    def clear_parameters(self):

        self.__parameters = {}
        self.__is_synchronized_with_server = False

    # Server methods

    def synchronize_parameters_by_id(self, id_observation):

        if self.__default_gateway is not None:
            server_parameters = self.__default_gateway.get_by_id(id_observation)

            if server_parameters is not None:
                self.__parameters = {**self.__parameters, **server_parameters[0]}
                self.__is_synchronized_with_server = True
            else:
                self.__is_synchronized_with_server = False

        return self.__is_synchronized_with_server

    def synchronize_parameters_by_parameters(self):
        server_parameters = None

        if self.__default_gateway is not None:

            search_parameters = {}
            for identifier_parameter in \
                    DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()]:

                check = False

                for key, value in self.__parameters.items():
                    if identifier_parameter in key:
                        search_parameters[key] = value
                        check = True

                if not check:
                    search_parameters = None
                    break

        if search_parameters is not None:
            entity = self.__default_gateway.get_by_parameters(search_parameters)
            if entity is not None and len(entity) == 1:
                server_parameters = entity[0]

        if server_parameters is not None:
            self.__parameters = {**self.__parameters, **server_parameters}
            self.__is_synchronized_with_server = True
        else:
            self.__is_synchronized_with_server = False

        return self.__is_synchronized_with_server

    def insert(self):
        result = None

        if not self.__is_synchronized_with_server:
            if all(any(identifier_parameter in str(parameter) for parameter in self.__parameters.keys())
                   for identifier_parameter
                   in DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()]):

                self.__default_gateway.insert(self.__parameters)
                result = self.synchronize_parameters_by_parameters()

                if result:
                    result = self.__parameters[self.__default_gateway.get_table_column_id_name()]

        return result

    def update(self, parameters_to_update={}):
        result = False

        if self.__is_synchronized_with_server:

            new_parameters = {**self.__parameters, **parameters_to_update}

            if self.__default_gateway is not None\
                    and all(any(identifier_parameter in parameter for identifier_parameter
                                in DefaultEntity.table_not_null_columns_names[self.__default_gateway.get_entry_point()])
                            for parameter in new_parameters.keys()):

                body = new_parameters
                identifier = self.__parameters[self.__default_gateway.get_table_column_id_name()]

                result = self.__default_gateway.update(identifier, body)

                if result is not None:
                    self.synchronize_parameters_by_id(identifier)

        else:
            self.__parameters = {**self.__parameters, **parameters_to_update}
            result = True

        return result

    def delete(self):
        result = False

        if self.__is_synchronized_with_server and self.__default_gateway is not None:

            id_measurement = self.__parameters[self.__default_gateway.get_table_column_id_name()]
            result = self.__default_gateway.delete(id_measurement)

            if result is not None:
                self.synchronize_parameters_by_id(id_measurement)

        return result
