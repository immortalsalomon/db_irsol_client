# Internal dependencies
from db_irsol.settings import Settings
from db_irsol.api_gateway.authenticate_gateway import AuthenticateGateway

# libraries dependencies
import requests
import json


class DefaultGateway:
    """ This class is used to communicate with the REST API service.
        It allows the use of functionalities related to the given entry point.
        The only functionalities it cannot provide are those related to authentication.

    :param entry_point: The name of the .php file, on the server, that handles the required requests or functionalities.
    :type entry_point: str
    :param consider_deleted_record: Whether to consider deleted records in requests.
    :type consider_deleted_record: bool
    :param consider_modified_record: Whether to consider modified (old version) records in requests.
    :type consider_modified_record: bool
    """

    def __init__(self, entry_point):
        """Constructor method
        """
        self.__entry_point = entry_point
        self.consider_deleted_record = False
        self.consider_modified_record = False

    #######################
    ### Offline Methods ###
    #######################

    def get_entry_point(self):
        """ Returns the name of the .php file, on the server, that handles the required requests or functionalities.
            The so called entry point set during object creation (in the constructor).

        :return: The name of the .php file, on the server, that handles the required requests or functionalities.
        :rtype: str
        """

        return self.__entry_point

    ######################
    ### Online Methods ###
    ######################

    # Get Methods

    def generic_get_request(self, params, authenticate_gateway=None):
        """ This method creates and sends all the get requests to the REST API service. By passing key parameters
            it is possible to choose which functionality to use from those provided by the REST API service.

        :param params: Dictionary containing all the parameters, and their values,
            that are to be sent via the GET request. All passed parameters are visible.
        :type params: dict
        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
        :return: If the response contains several records, it returns a list of records, represented as dictionaries.
            If the response returns only one record, it returns the record in the form of a dictionary.
        :rtype: list or dict
        """

        result = None
        body_data = {}

        if authenticate_gateway is None:
            print("authenticate gateway is none. The request will use the default user for authentication.")
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

        if len(body_data) > 0:

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
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
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
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
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
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
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
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
        :return: Returns a list containing all not null columns names in a table. The table from which the columns are
            taken is defined by the entry point set.
        :rtype: list
        """

        payload = {'get_table_not_null_columns_names': ""}
        return self.generic_get_request(payload, authenticate_gateway)

    def get_table_column_id_name(self):
        payload = {'get_table_column_id_name': ""}
        return self.generic_get_request(payload)

    def get_number_of_elements(self):
        payload = {'get_number_of_elements': ""}
        return self.generic_get_request(payload)

    def get_by_id(self, id_record):
        payload = {'id': id_record}
        return self.generic_get_request(payload)

    def get_chunk(self, start_element_number, number_of_elements):
        payload = {'start_element_number': start_element_number, 'number_of_elements': number_of_elements}
        return self.generic_get_request(payload)

    def get_by_parameters(self, columns_value_dict):
        return self.generic_get_request(columns_value_dict)

    def get_chunk_by_parameters(self,  start_element_number, number_of_elements, columns_value_dict):
        columns_value_dict['start_element_number'] = start_element_number
        columns_value_dict['number_of_elements'] = number_of_elements
        return self.generic_get_request(columns_value_dict)

    # POST METHODS

    def insert(self, columns_value_dict):
        result = None

        if self.authenticate_gateway is None:
            print("authenticate gateway is none. Not possible to authenticate on the server.")
            return result

        if self.authenticate_gateway.get_token() is None:
            print("token is none. The authenticate gateway can provide a token. Check the credentials in it.")
            return result

        auth_data = {'auth_token': self.authenticate_gateway.get_token()} if self.authenticate_gateway is not None else {}
        body_data = {**columns_value_dict, **auth_data}

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

    def update(self, id_record, columns_value_dict):
        result = None

        if self.authenticate_gateway is None:
            print("authenticate gateway is none. Not possible to authenticate on the server.")
            return result

        if self.authenticate_gateway.get_token() is None:
            print("token is none. The authenticate gateway can provide a token. Check the credentials in it.")
            return result

        payload = {'id': id_record}
        auth_data = {'auth_token': self.authenticate_gateway.get_token()} if self.authenticate_gateway is not None else {}
        body_data = {**columns_value_dict, **auth_data}

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

    def delete(self, id_record):
        result = False

        if self.authenticate_gateway is None:
            print("authenticate gateway is none. Not possible to authenticate on the server.")
            return result

        if self.authenticate_gateway.get_token() is None:
            print("token is none. The authenticate gateway can provide a token. Check the credentials in it.")
            return result

        payload = {'id': id_record}
        body_data = {'auth_token': self.authenticate_gateway.get_token()} if self.authenticate_gateway is not None else {}

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
