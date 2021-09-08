# Internal dependencies
from db_irsol.settings import Settings
from db_irsol.api_gateway.gateways.authenticate_gateway import AuthenticateGateway

# libraries dependencies
import requests
import json


class DefaultGateway:
    """ This class is used to communicate with the REST API service.
        It allows the use of functionalities related to the given entry point.
        The only functionalities it cannot provide are those related to authentication.

    :param entry_point: The name of the .php file, on the server, that handles the required requests or functionalities.
    :type entry_point: str
    :param consider_deleted_records: Whether to consider deleted records in requests.
    :type consider_deleted_records: bool
    :param consider_modified_records: Whether to consider modified (old version) records in requests.
    :type consider_modified_records: bool
    """

    def __init__(self, entry_point):
        """Constructor method
        """
        self.__entry_point = entry_point
        self.consider_deleted_records = False
        self.consider_modified_records = False

    #######################
    ### OFFLINE METHODS ###
    #######################

    def get_entry_point(self):
        """ Returns the name of the .php file, on the server, that handles the required requests or functionalities.
            The so called entry point set during object creation (in the constructor).

        :return: The name of the .php file, on the server, that handles the required requests or functionalities.
        :rtype: str
        """

        return self.__entry_point

    ######################
    ### ONLINE METHODS ###
    ######################

    # GET METHODS

    def generic_get_request(self, params, authenticate_gateway=None):
        """ This method creates and sends all the get requests to the REST API service. By passing key parameters
            it is possible to choose which functionality to use from those provided by the REST API service.

        :param params: Dictionary containing all the parameters, and their values,
            that are to be sent via the GET request. All passed parameters are visible.
        :type params: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: If the response contains several records, it returns a list of records, represented as dictionaries.
            If the response returns only one record, it returns the record in the form of a dictionary.
        :rtype: list or dict
        """

        result = None        # Search also modified and deleted records
        modified_deleted_records = {'consider_deleted_records': str(self.consider_deleted_records),
                                    'consider_modified_records': str(self.consider_modified_records)}
        params = {**params, **modified_deleted_records}
        body_data = {}

        if authenticate_gateway is None:
            print("The authenticate_gateway is None. The request will use the default user for authentication.")
            authenticate_gateway = AuthenticateGateway(Settings.AUTH_USERNAME, Settings.AUTH_PASSWORD)

        if authenticate_gateway.get_token() is None:
            print("Token is None. The authenticate gateway can not provide a token.")
            if not authenticate_gateway.are_credentials_valid():
                print("Credentials are not valid. The authenticate gateway can not authenticate on the server.")
            else:
                body_data['auth_username'] = authenticate_gateway.get_username()
                body_data['auth_password'] = authenticate_gateway.get_password()
        else:
            body_data['auth_token'] = authenticate_gateway.get_token()

        if 'auth_token' in body_data or ('auth_username' in body_data and 'auth_password' in body_data):

            # try to perform the request
            try:
                request = requests.get(Settings.api_url + "/" + self.__entry_point, params=params, json=body_data)

                # Convert string to list.
                parsed_result = json.loads(request.text[1:-1])

                if request.ok:
                    result = parsed_result
                elif 'error' in parsed_result:
                    print('Error arise: ' + parsed_result['error'])

            except requests.exceptions.ConnectionError:
                print("Connection to server "
                      + Settings.api_url
                      + " failed. Please check if the server is working or if you have internet connection.")
            except requests.exceptions.Timeout:
                print("Request timeout. Maybe set up for a retry, or continue in a retry loop.")
            except requests.exceptions.TooManyRedirects:
                print("Bad URL (" + Settings.api_url + "). Try a different one")
            except requests.exceptions.RequestException as e:
                print("Some error occur: \n" + str(e))
            except json.decoder.JSONDecodeError as e:
                print("There was a problem accessing the response: \n" + str(e))

        return result

    def get_info_table_columns(self, authenticate_gateway=None):
        """ This method returns information about the columns of a given table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: A list of dictionaries. Each of these contains the information of a column of the table related
            to the entry point set.
        :rtype: list
        """

        payload = {'get_info_table_columns': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_table_columns_names(self, authenticate_gateway=None):
        """ This method returns the names of the columns of a given table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list containing all column names in a table. The table from which the columns are
            taken is defined by the entry point set.
        :rtype: list
        """

        payload = {'get_table_columns_names': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_info_table_not_null_columns(self, authenticate_gateway=None):
        """ This method returns information about the not null columns of a given table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: A list of dictionaries. Each of these contains the information of a not null column of the table
            related to the entry point set.
        :rtype: list
        """

        payload = {'get_info_table_not_null_columns': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_table_not_null_columns_names(self, authenticate_gateway=None):
        """ This method returns the names of the not null columns of a given table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list containing all not null columns names in a table. The table from which the columns are
            taken is defined by the entry point set.
        :rtype: list
        """

        payload = {'get_table_not_null_columns_names': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_table_column_id_name(self, authenticate_gateway=None):
        """ This method returns the name of the column identifying the records in a table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a string containing the name of the column identifying the records in a table.
        :rtype: str
        """

        payload = {'get_table_column_id_name': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_number_of_elements(self, authenticate_gateway=None):
        """ This method returns the number of records in a table.
            The table from which the columns are taken is defined by the entry point set.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns the number of records in a table.
        :rtype: int
        """

        payload = {'get_number_of_elements': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_unique_identifier_columns(self, authenticate_gateway=None):
        payload = {'get_unique_identifier_columns': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_by_id(self, id_record, authenticate_gateway=None):
        """ This method returns the record, present in a table, that has the id passed as a parameter.
            The record is returned in the form of a dictionary.
            If no record has the id passed as the parameter, None is returned.
            The table from which the columns are taken is defined by the entry point set.

        :param id_record: The number defining the id of the record to be searched within
            the table defined by the entry point.
        :type id_record: int
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a dictionary containing all the fields, with their values,
            of the records with the id passed as a parameter.
        :rtype: dict
        """

        payload = {'id': id_record}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_chunk(self, start_element_number, number_of_elements, authenticate_gateway=None):
        """ This method returns a group of records of a table depending on the parameters passed to it as arguments.
            Each time the query extracts the records, it sorts the table in ascending ID order.
            The table from which the columns are taken is defined by the entry point set.

        :param start_element_number: This parameter defines from which position to start extracting records from
            the table. The range of this value goes from 0 to the total number of records in the table.
            The records are sorted by ascending ID.
        :type start_element_number: int
        :param number_of_elements: This parameter defines how many records to take starting from the
            initial position defined by the start_element_number parameter.
        :type number_of_elements: int
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list of dictionaries. Each dictionary contains the fields, with their values,
            of a single record.
        :rtype: list
        """

        payload = {'start_element_number': start_element_number, 'number_of_elements': number_of_elements}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_by_parameters(self, columns_value_dict, authenticate_gateway=None):
        """ This method returns all records of a table that have the same values as the fields defined
            in the dictionary passed to the method.
            The table from which the columns are taken is defined by the entry point set.

        :param columns_value_dict: Dictionary containing the fields, and their values,
            used to search for records in a table. In addition to the fields, it is
            possible to define comparators in the dictionary.
            For more information, see the documentation on the Wiki.
        :type columns_value_dict: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list of dictionaries. Each dictionary contains the fields, with their values,
            of a single record.
        :rtype: list
        """

        return self.generic_get_request(columns_value_dict, authenticate_gateway)

    def get_chunk_by_parameters(self,  start_element_number, number_of_elements, columns_value_dict,
                                authenticate_gateway=None):
        """ This method returns all records of a table that have the same values as the fields defined
            in the dictionary passed to the method. In addition, the records are filtered according to
            the range defined by the other parameters passed to the method. Each time the query extracts the records,
            it sorts the table in ascending ID order.
            The table from which the columns are taken is defined by the entry point set.

        :param start_element_number: This parameter defines from which position to start extracting records from
            the table. The range of this value goes from 0 to the total number of records in the table.
            The records are sorted by ascending ID.
        :type start_element_number: int
        :param number_of_elements: This parameter defines how many records to take starting from the
            initial position defined by the start_element_number parameter.
        :type number_of_elements: int
        :param columns_value_dict: Dictionary containing the fields, and their values,
            used to search for records in a table. In addition to the fields, it is
            possible to define comparators in the dictionary.
            For more information, see the documentation on the Wiki.
        :type columns_value_dict: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list of dictionaries. Each dictionary contains the fields, with their values,
            of a single record.
        :rtype: list
        """

        columns_value_dict['start_element_number'] = start_element_number
        columns_value_dict['number_of_elements'] = number_of_elements
        return self.generic_get_request(columns_value_dict, authenticate_gateway)

    # POST METHODS

    def insert(self, columns_value_dict, authenticate_gateway=None):
        """ This method allows a new record to be added to a database table.
            The fields, and their values, of the record to be added are defined in the dictionary passed to the method.
            The table from which the columns are taken is defined by the entry point set.

        :param columns_value_dict: Dictionary containing all the fields, and their values,
            of the record to be added to a database table.
        :type columns_value_dict: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns the number representing the id of the new record added to a database table.
        :rtype: int
        """

        result = None
        body_data = columns_value_dict

        if authenticate_gateway is not None:
            if authenticate_gateway.get_token() is None:
                print("Token is None. The authenticate gateway can not provide a token.")
                if not authenticate_gateway.are_credentials_valid():
                    print("Credentials are not valid. The authenticate gateway can not authenticate on the server.")
                else:
                    body_data['auth_username'] = authenticate_gateway.get_username()
                    body_data['auth_password'] = authenticate_gateway.get_password()
            else:
                body_data['auth_token'] = authenticate_gateway.get_token()
        else:
            print("The authenticate_gateway is None. Please provide one.")

        if 'auth_token' in body_data or ('auth_username' in body_data and 'auth_password' in body_data):

            # try to perform the request
            try:
                request = requests.post(Settings.api_url + "/" + self.__entry_point, json=body_data)

                if request.ok:
                    result = int(request.text.replace("\"", ""))
                else:
                    # Convert string to list.
                    parsed_result = json.loads(request.text[1:-1])
                    if 'error' in parsed_result:
                        print('Error arise: ' + str(parsed_result['error']))

            except requests.exceptions.ConnectionError:
                print("Connection to server "
                      + Settings.api_url
                      + " failed. Please check if the server is working or if you have internet connection.")
            except requests.exceptions.Timeout:
                print("Request timeout. Maybe set up for a retry, or continue in a retry loop.")
            except requests.exceptions.TooManyRedirects:
                print("Bad URL (" + Settings.api_url + "). Try a different one")
            except requests.exceptions.RequestException as e:
                print("Some error occur: \n" + str(e))
            except json.decoder.JSONDecodeError as e:
                print("There was a problem accessing the response: \n" + str(e))

        return result

    # PUT METHODS

    def update(self, id_record, columns_value_dict, authenticate_gateway=None):
        """ This method is used to update a record in a table according to the parameters passed to it.
            The table from which the columns are taken is defined by the entry point set.

        :param id_record: The number representing the ID of a record in a table that you wish to update.
        :type id_record: int
        :param columns_value_dict: Dictionary containing the fields, and their values,
            that you wish to update for a given record in a table.
        :type columns_value_dict: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns the number representing the id of the updated record of a table.
        :rtype: int
        """

        result = None
        body_data = columns_value_dict
        payload = {'id': id_record}

        if authenticate_gateway is not None:
            if authenticate_gateway.get_token() is None:
                print("Token is None. The authenticate gateway can not provide a token.")
                if not authenticate_gateway.are_credentials_valid():
                    print("Credentials are not valid. The authenticate gateway can not authenticate on the server.")
                else:
                    body_data['auth_username'] = authenticate_gateway.get_username()
                    body_data['auth_password'] = authenticate_gateway.get_password()
            else:
                body_data['auth_token'] = authenticate_gateway.get_token()
        else:
            print("The authenticate_gateway is None. Please provide one.")

        if 'auth_token' in body_data or ('auth_username' in body_data and 'auth_password' in body_data):

            # try to perform the request
            try:
                request = requests.put(Settings.api_url + "/" + self.__entry_point, json=body_data, params=payload)

                if request.ok:
                    result = int(request.text.replace("\"", ""))
                else:
                    # Convert string to list.
                    parsed_result = json.loads(request.text[1:-1])
                    if 'error' in parsed_result:
                        print('Error arise: ' + parsed_result['error'])

            except requests.exceptions.ConnectionError:
                print("Connection to server "
                      + Settings.api_url
                      + " failed. Please check if the server is working or if you have internet connection.")
            except requests.exceptions.Timeout:
                print("Request timeout. Maybe set up for a retry, or continue in a retry loop.")
            except requests.exceptions.TooManyRedirects:
                print("Bad URL (" + Settings.api_url + "). Try a different one")
            except requests.exceptions.RequestException as e:
                print("Some error occur: \n" + str(e))
            except json.decoder.JSONDecodeError as e:
                print("There was a problem accessing the response: \n" + str(e))

        return result

    # DELETE METHODS

    def delete(self, id_record, authenticate_gateway=None):
        """ This method is used to delete a record in a table according to the id parameter passed to it.
            The table from which the columns are taken is defined by the entry point set.

        :param id_record: The number representing the ID of a record in a table that you wish to delete.
        :type id_record: int
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.gateways.authenticate_gateway.AuthenticateGateway`
        :return: Returns True if the record was deleted. While it returns False if the record could not be deleted.
        :rtype: bool
        """

        result = False
        body_data = {}
        payload = {'id': id_record}

        if authenticate_gateway is not None:
            if authenticate_gateway.get_token() is None:
                print("Token is None. The authenticate gateway can not provide a token.")
                if not authenticate_gateway.are_credentials_valid():
                    print("Credentials are not valid. The authenticate gateway can not authenticate on the server.")
                else:
                    body_data['auth_username'] = authenticate_gateway.get_username()
                    body_data['auth_password'] = authenticate_gateway.get_password()
            else:
                body_data['auth_token'] = authenticate_gateway.get_token()
        else:
            print("The authenticate_gateway is None. Please provide one.")

        if 'auth_token' in body_data or ('auth_username' in body_data and 'auth_password' in body_data):

            # try to perform the request
            try:
                request = requests.delete(Settings.api_url + "/" + self.__entry_point, params=payload, json=body_data)

                if request.ok:
                    result = True
                else:
                    # Convert string to list.
                    parsed_result = json.loads(request.text[1:-1])
                    if 'error' in parsed_result:
                        print('Error arise: ' + parsed_result['error'])

            except requests.exceptions.ConnectionError:
                print("Connection to server "
                      + Settings.api_url
                      + " failed. Please check if the server is working or if you have internet connection.")
            except requests.exceptions.Timeout:
                print("Request timeout. Maybe set up for a retry, or continue in a retry loop.")
            except requests.exceptions.TooManyRedirects:
                print("Bad URL (" + Settings.api_url + "). Try a different one")
            except requests.exceptions.RequestException as e:
                print("Some error occur: \n" + str(e))
            except json.decoder.JSONDecodeError as e:
                print("There was a problem accessing the response: \n" + str(e))

        return result
