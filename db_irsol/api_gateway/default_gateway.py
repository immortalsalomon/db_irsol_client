# Internal dependencies
from db_irsol.settings import Settings

# libraries dependencies
import requests
import json


class DefaultGateway:

    def __init__(self, entry_point, authenticate_gateway=None):
        self.__entry_point = entry_point
        self.consider_deleted_record = False
        self.consider_modified_record = False
        self.authenticate_gateway = authenticate_gateway

    def get_entry_point(self):
        return self.__entry_point

    # GET METHODS

    def generic_get_request(self, params):
        result = None

        if self.authenticate_gateway is None:
            print("authenticate gateway is none. Not possible to authenticate on the server.")
            return result

        if self.authenticate_gateway.get_token() is None:
            print("token is none. The authenticate gateway can provide a token. Check the credentials in it.")
            return result

        body_data = {'auth_token': self.authenticate_gateway.get_token()} if self.authenticate_gateway is not None else {}

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

    def get_info_table_columns(self):
        payload = {'get_info_table_columns': ""}
        return self.generic_get_request(payload)

    def get_table_columns_names(self):
        payload = {'get_table_columns_names': ""}
        return self.generic_get_request(payload)

    def get_info_table_not_null_columns(self):
        payload = {'get_info_table_not_null_columns': ""}
        return self.generic_get_request(payload)

    def get_table_not_null_columns_names(self):
        payload = {'get_table_not_null_columns_names': ""}
        return self.generic_get_request(payload)

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
