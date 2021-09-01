

class Settings:

    # Authentication data.
    # Only have the possibility to see the data not to create.
    AUTHENTICATE_USERNAME = 'db_irsol_client'
    AUTHENTICATE_PASSWORD = 'U{4ZA;Z<j]rYH~2`'

    # This variable is use by the entities
    # This variable tells which measurements to ignore and which not.
    # This list can contains only part of the names of the measurements.
    # The filter on which measurements to ignore is done on their names.
    measurements_ignore_keys_words = [
        'cal',
        'dark'
    ]

    # This variables are use by the gateways
    # URL of the server. The entry point is always the api folder.
    api_url = "http://localhost/api"
    # The following variable is used to check the duration of the token.
    # The time defined by the following variable is used as range to tell if the expire time of a token is close.
    # If the time of expire is more close than the time defined by the following constant the token is regenerate.
    token_timestamp_expiration_security = 10

    # This variables are use by the parsers
    # They define the fields that need to be taken from the measurements files.
    # Each fields name has its corresponding column name in the database.
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

    # The following list contains all the entry points present on the server.
    ENTRY_POINTS = ["Observation.php", "Measurement.php"]
