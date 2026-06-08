from datetime import timedelta

DOMAIN = "powafree_cloud"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

# Intervallo di polling per i dati dei sensori (per evitare ban)
UPDATE_INTERVAL = timedelta(seconds=60)

# API Base URL
BASE_URL = "http://www.powafree.com"

# Nomi costanti usati nell'API
API_LOGIN = "/api/user/login/email"
API_DEVICE_LIST = "/api/devices/list"
API_DEVICE_INFO = "/api/devices/info"
API_DEVICE_LAST_DATA = "/api/devices/last_data"
API_DEVICE_DATA = "/api/devices/data"

# Comandi dedotti (setter)
API_DEVICE_SET = "/api/devices/set_config" # Questo sarà da verificare empiricamente, solitamente è config_set o set_config. Se non c'è, adatteremo.
