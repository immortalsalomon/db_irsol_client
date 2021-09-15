# Internal dependencies
from db_irsol.settings import Settings
from db_irsol.api_gateway.gateways.default_gateway import DefaultGateway
from db_irsol.api_gateway.gateways.authenticate_gateway import AuthenticateGateway


class GatewayManager:
    """ This class is used to manage all gateway objects that communicate with the REST API service.
        It simplifies the management of gateways.

    :param username: The user name used for authentication.
    :type username: str
    :param password: The password of the username used for authentication.
    :type password: str
    :param default_gateways: A dictionary containing a
        class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`object for each entry point defined in
        the package settings file. Each gateway handles requests for a specific table.
    :type default_gateways: dict
    :param is_authentication_working: This variable shows whether the gateway manager is able to
        authenticate to in the REST API service.
    :type is_authentication_working: bool
    :param authenticate_gateway: The object of the
        class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
        in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
        class provides the information (token, user credentials) for authentication.
    :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
    """

    def __init__(self, username=None, password=None, entry_points=None):
        """Constructor method
        """
        self.__username = None
        self.__password = None
        self.__authenticate_gateway = None
        self.__is_authentication_working = False

        if username is not None and password is not None and username != "" and password != "":
            self.set_credentials(username, password)

        self.__default_gateways = {}
        if entry_points is not None:
            self.set_default_gateways(entry_points)
        else:
            self.set_default_gateways()

    #######################
    ### OFFLINE METHODS ###
    #######################

    # SET METHODS

    def set_credentials(self, username, password):
        """ This method allows to set up a new user to make requests to the REST API service.

        :param username: The user name used for authentication.
        :type username: str
        :param password: The password of the username used for authentication.
        :type password: str
        """

        tmp_authenticate_gateway = AuthenticateGateway(username, password)
        if tmp_authenticate_gateway.are_credentials_valid():
            self.__authenticate_gateway = tmp_authenticate_gateway
            self.__username = username
            self.__password = password
            self.__is_authentication_working = True
        else:
            print("The passed credentials are not valid.")

    def set_authenticate_gateway(self, authenticate_gateway):
        """ This method allows to set up a new user to make requests to the REST API service.
            The new user is set up using data from the authenticate gateway object passed to the method.

        :param authenticate_gateway: The object of the
            class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway` class that allows authentication
            in the REST API service. The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :type authenticate_gateway: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
        """

        if authenticate_gateway.are_credentials_valid():
            self.__authenticate_gateway = authenticate_gateway
            self.__username = authenticate_gateway.get_username()
            self.__password = authenticate_gateway.get_password()
            self.__is_authentication_working = True
        else:
            print("The passed authenticate_gateway is not valid.")

    def set_default_gateways(self, entry_points=Settings.ENTRY_POINTS):
        """ This method allows to create a class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`
            object for each entry point passed to it.

        :param entry_points: List containing the names of all the entry points for which it is intended
            to create a class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`
            object to communicate with the REST API service. The default value is the list
            of entry points defined in the settings file.
        :type entry_points: list
        """

        self.__default_gateways = {}
        for entry_point in entry_points:
            self.__default_gateways[entry_point] = DefaultGateway(entry_point)

    def set_consider_deleted_records(self, value):

        if self.__default_gateways is not None:
            for key, default_gateway in self.__default_gateways.items():
                default_gateway.consider_deleted_records = value

    def set_consider_modified_records(self, value):

        if self.__default_gateways is not None:
            for key, default_gateway in self.__default_gateways.items():
                default_gateway.consider_modified_records = value

    # GET METHODS

    def get_username(self):
        """ This method returns the user name used for authentication.

        :return: A string containing the user name.
        :rtype: str
        """

        return self.__username

    def get_password(self):
        """ This method returns the password of the username used for authentication.

        :return: A string containing the password of the user.
        :rtype: str
        """

        return self.__password

    def get_authenticate_gateway(self):
        """ This method returns the authenticate_gateway of the username used for authentication.

        :return: The object of the class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class that allows authentication in the REST API service.
            The class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
            class provides the information (token, user credentials) for authentication.
        :rtype: class:`db_irsol.api_gateway.authenticate_gateway.AuthenticateGateway`
        """

        return self.__authenticate_gateway

    def get_default_gateways(self):
        """ This method returns a dictionary containing all
            class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`
            objects created for all passed entry points.

        :return: A dictionary containing all class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`
            objects created for all passed entry points.
        :rtype: dict
        """

        return self.__default_gateways

    def get_default_gateway(self, entry_point):
        """ This method returns a default gateway object of the entry point passed to it as a parameter.

        :return: Returns a class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway` object
            of the entry point passed to it as a parameter.
        :rtype: class:`db_irsol.api_gateway.gateways.default_gateway.DefaultGateway`
        """

        result = None

        if entry_point in self.__default_gateways:
            result = self.__default_gateways[entry_point]

        return result

    def get_is_authentication_working(self):
        """ This method returns True if authentication in the REST API service works. If not, it returns False.

        :return: Returns True if authentication in the REST API service works. If not, it returns False.
        :rtype: bool
        """

        return self.__is_authentication_working
