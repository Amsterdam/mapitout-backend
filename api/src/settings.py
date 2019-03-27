import configparser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config_auth = configparser.ConfigParser()
config_auth.read(os.path.join(BASE_DIR, "config.ini"))

TESTING = {"running": False}

ENVIRONMENT_OVERRIDES = [
    ('host', os.getenv('DATABASE_HOST', 'database')),
    ('port', os.getenv('DATABASE_PORT', '5432')),
    ('database', os.getenv('DATABASE_NAME', 'mapitout')),
    ('username', os.getenv('DATABASE_USER', 'mapitout')),
    ('password', os.getenv('DATABASE_PASSWORD', 'insecure')),
]

VERIFY_SSL = os.getenv('ADP_USE_SSL_CERT', False)
