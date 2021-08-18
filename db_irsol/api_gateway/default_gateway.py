# Internal package dependencies
import db_irsol.api_gateway.constants as constants

# libraries dependencies
import requests
import json


class DefaultGateway:

    def __init__(self, entry_point, authenticate_gateway=None):
        self.__entry_point = entry_point
        self.consider_deleted_record = False
        self.consider_modified_record = False
        self.authenticateGateway = authenticate_gateway

    # GET METHODS

    def get_info_table_columns(self):
        payload = {'get_info_table_columns': ""}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])

        return result

    def get_table_columns_names(self):
        payload = {'get_table_columns_names': ""}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])

        return result

    def get_info_table_not_null_columns(self):
        payload = {'get_info_table_not_null_columns': ""}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])

        return result

    def get_table_not_null_columns_names(self):
        payload = {'get_table_not_null_columns_names': ""}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])

        return result

    def get_number_of_elements(self):
        payload = {'get_number_of_elements': ""}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])

        return result

    def get_by_id(self, id_record):
        payload = {'id': id_record}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        record = None
        if request.ok:
            # Return a list of records. Because the id is unique take the first one
            record = json.loads(request.text[1:-1])[0]

        return record

    def get_chunk(self, start_element_number, number_of_elements):
        payload = {'start_element_number': start_element_number, 'number_of_elements': number_of_elements}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        records = None

        if request.ok:
            # Return a list of records.
            records = json.loads(request.text[1:-1])

        return records

    def get_by_parameters(self, columns_value_dict):
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=columns_value_dict, json=body_data)

        records = None

        if request.ok:
            # Return a list of records.
            records = json.loads(request.text[1:-1])

        return records

    def get_chunk_by_parameters(self,  start_element_number, number_of_elements, columns_value_dict):
        columns_value_dict['start_element_number'] = start_element_number
        columns_value_dict['number_of_elements'] = number_of_elements
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.get(constants.API_URL + "/" + self.__entry_point, params=columns_value_dict, json=body_data)

        records = None
        print(request.url)

        if request.ok:
            # Return a list of records.
            records = json.loads(request.text[1:-1])

        return records

    # POST METHODS

    def insert(self, columns_value_dict):
        auth_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        body_data = {**columns_value_dict, **auth_data}
        request = requests.post(constants.API_URL + "/" + self.__entry_point, json=body_data)

        result = None

        if request.ok:
            # Return a list of records.
            result = int(request.text.replace("\"", ""))

        return result

    # PUT METHODS

    def update(self, id_record, columns_value_dict):
        payload = {'id': id_record}
        auth_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        body_data = {**columns_value_dict, **auth_data}
        request = requests.put(constants.API_URL + "/" + self.__entry_point, json=body_data, params=payload)

        result = None
        if request.ok:
            # Return a list of records.
            result = int(request.text.replace("\"", ""))

        return result

    # DELETE METHODS

    def delete(self, id_record):
        payload = {'id': id_record}
        body_data = {'auth_token': self.authenticateGateway.get_token()} if self.authenticateGateway is not None else {}
        request = requests.delete(constants.API_URL + "/" + self.__entry_point, params=payload, json=body_data)

        return request.ok
