# Internal dependencies
from db_irsol.api_gateway.gateways.authenticate_gateway import AuthenticateGateway
from db_irsol.api_gateway.gateways.default_gateway import DefaultGateway
from db_irsol.api_gateway.gateway_manager import GatewayManager


class GatewayFunctions:

    ###########################################
    ### Pre build function for authenticate ###
    ###########################################

    # This functions return the authenticate gateway. It allows the authentication on the server.
    @staticmethod
    def get_authenticate_gateway(username, password):
        return AuthenticateGateway(username, password)

    ##############################################
    ### Pre build function for a table gateway ###
    ##############################################

    # This function return a default gateway that allows to access the data on the server of the specific entry point.
    @staticmethod
    def get_default_gateway(entry_point):
        return DefaultGateway(entry_point)

    ################################################
    ### Pre build functions for gateways manager ###
    ################################################

    # This function return a manager gateway that manages all the default gateway instance for all the
    # entry points defined in settings file.
    @staticmethod
    def get_gateways_manager_with_authenticate_gateway(authenticate_gateway):
        manager = GatewayManager()
        manager.set_authenticate_gateway(authenticate_gateway)
        return manager

    # This function return a manager gateway that manages all the default gateway instance for all the
    # entry points defined in settings file.
    @staticmethod
    def get_gateways_manager_with_credentials(username, password):
        manager = GatewayManager(username, password)
        return manager
