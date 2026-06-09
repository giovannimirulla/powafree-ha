from datetime import timedelta

DOMAIN = "powafree_cloud"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

# Intervallo di polling per i dati dei sensori (per evitare ban)
UPDATE_INTERVAL = timedelta(seconds=60)

# API Base URL
BASE_URL = "http://www.powafree.com"

# ── Endpoint API completi (estratti da ApiService.java via JADX) ──

# Autenticazione
API_LOGIN = "/api/user/login/email"
API_USER_REGISTER = "/api/user/register"
API_USER_SEND_CODE = "/api/user/send_code"
API_USER_VERIFY_CODE = "/api/user/verify_code"
API_USER_RESET_PASSWORD = "/api/user/reset_password"
API_USER_DELETE = "/api/user/delete"
API_USER_UPDATE_PROFILE = "/api/user/update_profile"
API_USER_REGION = "/api/user/region"

# Dispositivi - Lettura
API_DEVICE_LIST = "/api/devices/list"
API_DEVICE_INFO = "/api/devices/info"
API_DEVICE_LAST_DATA = "/api/devices/last_data"
API_DEVICE_DATA = "/api/devices/data"
API_DEVICE_STATUS = "/api/devices/status"
API_DEVICE_IS_BOUND = "/api/devices/is_bound"

# Dispositivi - Configurazione
API_DEVICE_CONFIG_DOWNLOAD = "/api/devices/setting/download"
API_DEVICE_SET = "/api/devices/setting/upload"

# Dispositivi - Gestione
API_DEVICE_BIND = "/api/devices/bind"
API_DEVICE_BIND_SLAVE = "/api/devices/bind/slave"
API_DEVICE_UNBIND = "/api/devices/unbind"
API_DEVICE_SHARE = "/api/devices/share"

# OTA (Firmware Update)
API_DEVICE_OTA_INFOS = "/api/devices/ota_infos"
API_DEVICE_OTA_STATUS = "/api/devices/ota_status"

# Altro
API_FEEDBACK = "/api/feedback"
API_UPLOAD_FILE = "/common/upload/file"
