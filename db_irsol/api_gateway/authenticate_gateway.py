# Internal dependencies
from db_irsol.settings import Settings

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
        if self.__token is not None:
            self.__token_expiration_time = jwt.decode(self.__token, options={"verify_signature": False})['exp'] \
                if self.__token is not None else None
        else:
            self.__token_expiration_time = None

    def get_token(self):

        if self.__token is not None and \
                time.time() >= self.__token_expiration_time + Settings.token_timestamp_expiration_security:
            self.__token = self.get_token()
            if self.__token is not None:
                self.__token_expiration_time = jwt.decode(self.__token, options={"verify_signature": False})['exp']

        return self.__token

    def get_username(self):
        return self.__auth_data['auth_username']

    def get_password(self):
        return self.__auth_data['auth_password']

    def get_expiration_time(self):
        return self.__token_expiration_time

    # GET REQUESTS

    def are_credentials_valid(self):
        result = False

        payload = {'validate_credentials': ""}

        # try to perform the request
        try:
            request = requests.get(Settings.api_url + "/" + AuthenticateGateway.entry_point, params=payload,
                                   json=self.__auth_data)

            # Convert string to list.
            parsed_result = json.loads(request.text[1:-1])

            if request.ok:
                result = True
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

    def is_token_valid(self):
        result = False

        if self.get_token() is None:
            print("token is none")
            return result

        payload = {'validate_token': ""}
        body_data = {'auth_token': self.__token}

        # try to perform the request
        try:
            request = requests.get(Settings.api_url + "/" + AuthenticateGateway.entry_point, params=payload,
                                   json=body_data)

            # Convert string to list.
            parsed_result = json.loads(request.text[1:-1])

            if request.ok:
                result = True
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

    def generate_token(self):
        result = None

        # Dictionary containing all the params value.
        payload = {'get_token': ""}

        # try to perform the request
        try:
            request = requests.get(Settings.api_url + "/" + AuthenticateGateway.entry_point, params=payload,
                                   json=self.__auth_data)

            # Convert string to list.
            parsed_result = json.loads(request.text[1:-1])

            if request.ok:
                result = parsed_result['token']
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
