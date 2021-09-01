# Internal dependencies
from db_irsol.settings import Settings
from db_irsol.api_gateway.default_gateway import DefaultGateway
from db_irsol.api_gateway.authenticate_gateway import AuthenticateGateway


class GatewayManager:

    def __init__(self):
        self.__username = None
        self.__password = None
        self.__authenticate_gateway = None
        self.__default_gateways = {}

    # Set methods

    def set_credentials(self, username, password):
        self.__authenticate_gateway = AuthenticateGateway(username, password)
        self.set_default_gateways()

    def set_authenticate_gateway(self, authenticate_gateway):
        self.__authenticate_gateway = authenticate_gateway
        self.set_default_gateways()

    def set_default_gateways(self, entry_points=Settings.ENTRY_POINTS):

        if self.__authenticate_gateway is not None:
            self.__default_gateways = {}
            for entry_point in entry_points:
                self.__default_gateways[entry_point] = DefaultGateway(entry_point, self.__authenticate_gateway)

    # Get methods

    def get_credentials(self):
        return self.__username, self.__password

    def get_authenticate_gateway(self):
        return self.__authenticate_gateway

    def get_default_gateways(self):
        return self.__default_gateways

    def get_default_gateway(self, entry_point):
        result = None

        if entry_point in self.__default_gateways:
            result = self.__default_gateways[entry_point]

        return result
