

class Settings:
    """ This class contains all the settings needed for the db_irsol package to work.
        Some settings can be changed, others cannot.

    :param AUTH_USERNAME: The user name of the standard user.
        This user only has permission to view all data except the other users data.
    :type AUTH_USERNAME: str, constant
    :param AUTH_PASSWORD: The password of the standard user.
        This user only has permission to view all data except the other users data.
    :type AUTH_PASSWORD: str, constant
    :param keywords_to_ignore_measurements: List of keywords that can be contained in the names of the measurements.
        If the name of a measurement contains one or more of these keywords, the measurement is ignored.
        The default values are "dark" and "cal".
    :type keywords_to_ignore_measurements: list
    :param api_url: The URL where the REST API service of the IRSOL database can be reached.
    :type api_url: str
    :param token_timestamp_expiration_security: The number is used as time range to check if the expire time
        of a token is close. If the time of expire is more close than the time defined by this variable the token is
        regenerate. The set number represents a time range in seconds.
    :type token_timestamp_expiration_security: int
    :param FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES: It define the fields that need to be taken from
        a .z3db measurement file. The keys are the fields names that can be present in a measurement file.
        While the values are the respective column names in the database.
    :type FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES: dict, constant
    :param FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES: It define the fields that need to be taken from
        a .fits measurement file. The keys are the fields names that can be present in a measurement file.
        While the values are the respective column names in the database.
    :type FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES: dict, constant
    :param ENTRY_POINTS: List of entry points provide by the REST API service. Each entry point is the name of
        the file .php, present on the server, that processes a specific set of requests. The requests are divided
        in set based on the entity (Observation, Measurement, Telescope, ...) they will work with.
    :type ENTRY_POINTS: list, constant
    """

    AUTH_USERNAME = 'db_irsol_client'
    AUTH_PASSWORD = 'U{4ZA;Z<j]rYH~2`'

    keywords_to_ignore_measurements = [
        'cal',
        'dark'
    ]

    api_url = "https://db.irsol.ch/api"

    token_timestamp_expiration_security = 10

    FIELDS_NAMES_Z3BD_FILE_TO_DATABASE_COLUMNS_NAMES = {
        'CAM_IT': 'cam_it',
        'CAM_TC': 'cam_tc',
        'DATE': 'start_datetime',
        'DATE_END': 'end_datetime',
        'PIGI': 'pigi',
        'WLENGTH': 'wlength',
        'IMG_TYPE': 'img_type',
        'IMG_TYPX': 'img_typx',
        'IMG_TYPY': 'img_typy',
        'M_TYPE': 'm_type',
        'OBSERVER': 'observer',
        'TELESCOP': 'fk_telescope-name'
    }

    FIELDS_NAMES_FITS_FILE_TO_DATABASE_COLUMNS_NAMES = {
        'CAM_IT': 'cam_it',
        'IT': 'cam_it',
        'CAM_TC': 'cam_tc',
        'TC': 'cam_tc',
        'DATE': 'start_datetime',
        'PIGI': 'pigi',
        'WLENGTH': 'wlength',
        'IMG_T': 'img_type',
        'M_TYPE': 'm_type',
        'OBSERVER': 'observer',
        'TELESCOP': 'fk_telescope-name'
    }

    ENTRY_POINTS = ["Observation.php", "Measurement.php"]
