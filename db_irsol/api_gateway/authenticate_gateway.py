# Internal package dependencies
import db_irsol.api_gateway.constants as constants

# libraries dependencies
import requests
import json
import jwt
import time


class AuthenticateGateway:
    entry_point = 'Authenticate'

    def __init__(self, auth_username, auth_password):
        self.__auth_data = {'auth_username': auth_username,
                            'auth_password': auth_password}

        self.__token = self.generate_token()
        self.__token_expiration_time = jwt.decode(self.__token, options={"verify_signature": False})['exp'] \
            if self.__token is not None else None

    def get_token(self):

        if self.__token is not None and \
                time.time() >= self.__token_expiration_time + constants.TOKEN_TIMESTAMP_EXPIRATION_SECURITY:
            self.__token = self.get_token()
            if self.__token is not None:
                self.__token_expiration_time = jwt.decode(self.__token, options={"verify_signature": False})['exp']

        return self.__token

    def get_username(self):
        return self.__auth_data['auth_username']

    def get_password(self):
        return self.__auth_data['auth_password']

    # GET REQUESTS

    def are_credentials_valid(self):
        payload = {'validate_credentials': ""}
        request = requests.get(constants.API_URL + "/" + AuthenticateGateway.entry_point, params=payload, json=self.__auth_data)

        result = False
        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])
            result = True

        return result

    def is_token_valid(self):
        payload = {'validate_token': ""}
        body_data = {'auth_token': self.__token}
        request = requests.get(constants.API_URL + "/" + AuthenticateGateway.entry_point, params=payload, json=body_data)

        result = False

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])
            result = True

        return result

    def generate_token(self):
        payload = {'get_token': ""}
        request = requests.get(constants.API_URL + "/" + AuthenticateGateway.entry_point, params=payload,
                               json=self.__auth_data)

        result = None

        if request.ok:
            # Convert string to list.
            result = json.loads(request.text[1:-1])
            if 'token' in result:
                result = result['token']

        return result
