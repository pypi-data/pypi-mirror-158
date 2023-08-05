''' 
MariaDB client flags (internal use only).

These flags are used when establishing a connection to a MariaDB
database server or to check the capabilities of a MariaDB server.

Client flags are defined in module *mariadb.constants.CLIENT_FLAG*
'''

MYSQL = 1  # MariaDB
LONG_PASSWORD= 1 # MySQL
FOUND_ROWS = 2
LONG_FLAG = 4
CONNECT_WITH_DB	= 8
NO_SCHEMA = 16
COMPRESS = 32
LOCAL_FILES = 128
IGNORE_SPACE = 256
INTERACTIVE	= 1024
SSL = 2048
TRANSACTIONS = 8192
SECURE_CONNECTION = 32768  
MULTI_STATEMENTS = 1 << 16
MULTI_RESULTS = 1 << 17
PS_MULTI_RESULTS = 1 << 18
PLUGIN_AUTH = 1 << 19
CONNECT_ATTRS = 1 << 20
CAN_HANDLE_EXPIRED_PASSWORDS = 1 < 22
SESSION_TRACKING = 1 << 23
SSL_VERIFY_SERVER_CERT = 1 << 30
REMEMBER_OPTIONS = 1 << 31

# MariaDB specific capabilities
PROGRESS = 1 << 32
BULK_OPERATIONS = 1 << 34
EXTENDED_METADATA = 1 << 35
CACHE_METDATA = 1 << 36
