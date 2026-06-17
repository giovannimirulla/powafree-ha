import logging
import time
import aiohttp
from typing import Any, Dict, List

from .const import BASE_URL, API_LOGIN, API_DEVICE_LIST, API_DEVICE_LAST_DATA

_LOGGER = logging.getLogger(__name__)

class PowafreeApiClientError(Exception):
    """Exception to indicate a general API error."""

class PowafreeAuthError(PowafreeApiClientError):
    """Exception to indicate an authentication error."""

class PowafreeApiClient:
    def __init__(self, email: str, password: str, session: aiohttp.ClientSession) -> None:
        self._email = email
        self._password = password
        self._session = session
        self._token = None
        self._user_id = None
        self._ble_mac = None

    async def _request(self, endpoint: str, data: Dict[str, Any] = None, require_auth: bool = True) -> Dict[str, Any]:
        """Wrapper for API requests."""
        url = f"{BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if require_auth:
            if not self._token:
                await self.login()
            headers["Authorization"] = self._token

        try:
            async with self._session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                json_data = await response.json()
                
                if json_data.get("code") != 0:
                    msg = json_data.get("message", "Unknown error")
                    if "token" in msg.lower() or json_data.get("code") == 401:
                        raise PowafreeAuthError(f"Auth error: {msg}")
                    raise PowafreeApiClientError(f"API Error: {msg}")
                    
                return json_data.get("data", json_data)
                
        except aiohttp.ClientError as err:
            raise PowafreeApiClientError(f"Error communicating with API: {err}")

    async def login(self) -> bool:
        """Login and get token."""
        data = {
            "email": self._email,
            "password": self._password
        }
        try:
            response = await self._request(API_LOGIN, data=data, require_auth=False)
            self._token = response.get("token")
            self._user_id = response.get("userId")
            
            if not self._token or not self._user_id:
                raise PowafreeAuthError("No token or user id returned.")
            
            return True
        except Exception as e:
            _LOGGER.error("Login failed: %s", e)
            raise PowafreeAuthError(str(e))

    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get list of devices."""
        if not self._user_id:
            await self.login()
            
        data = {"userId": self._user_id}
        response = await self._request(API_DEVICE_LIST, data=data)
        
        if isinstance(response, list):
            if response:
                self._ble_mac = response[0].get("bleMac")
            return response
        return []

    async def get_last_data(self, ble_mac: str = None) -> Dict[str, Any]:
        """Get latest telemetry data for a device."""
        target_mac = ble_mac or self._ble_mac
        if not target_mac:
            await self.get_devices()
            target_mac = self._ble_mac
            
        if not target_mac or not self._user_id:
            raise PowafreeApiClientError("No device found to poll.")
            
        data = {
            "userId": self._user_id,
            "bleMac": target_mac
        }
        
        response = await self._request(API_DEVICE_LAST_DATA, data=data)
        return response

    async def get_config(self, ble_mac: str = None) -> Dict[str, Any]:
        """Download the full device configuration (setting/download)."""
        target_mac = ble_mac or self._ble_mac
        if not target_mac:
            await self.get_devices()
            target_mac = self._ble_mac

        data = {
            "userId": self._user_id,
            "bleMac": target_mac
        }

        response = await self._request("/api/devices/setting/download", data=data)
        return response if isinstance(response, dict) else {}

    async def get_device_info(self, ble_mac: str = None) -> Dict[str, Any]:
        """Get device info (firmware versions, wifi status)."""
        target_mac = ble_mac or self._ble_mac
        data = {
            "userId": self._user_id,
            "bleMac": target_mac
        }
        response = await self._request("/api/devices/info", data=data)
        return response if isinstance(response, dict) else {}

    async def get_device_status(self, ble_mac: str = None) -> Any:
        """Get device WiFi status."""
        target_mac = ble_mac or self._ble_mac
        data = {
            "userId": self._user_id,
            "bleMac": target_mac
        }
        return await self._request("/api/devices/status", data=data)

    async def get_historical_data(self, ble_mac: str = None) -> Any:
        """Get historical device data (api/devices/data)."""
        target_mac = ble_mac or self._ble_mac
        data = {
            "userId": self._user_id,
            "bleMac": target_mac
        }
        return await self._request("/api/devices/data", data=data)

    async def set_config(self, ble_mac: str, key: str, value: Any) -> bool:
        """
        Send a command to the device using the correct YtDeviceConfig schema.
        L'API richiede l'oggetto di configurazione COMPLETO, quindi prima scarichiamo,
        poi modifichiamo il parametro, e infine ricarichiamo tutto.
        """
        from .const import API_DEVICE_SET
        target_mac = ble_mac or self._ble_mac
        base_req = {
            "userId": self._user_id,
            "bleMac": target_mac
        }
        
        # 1. Scarica la configurazione attuale
        try:
            current_config = await self._request("/api/devices/setting/download", data=base_req)
        except Exception as e:
            _LOGGER.error("Errore nel download della configurazione: %s", e)
            return False
            
        if not isinstance(current_config, dict):
            _LOGGER.error("Formato configurazione inatteso: %s", current_config)
            return False

        # 2. Modifica il parametro richiesto
        current_config[key] = value
        
        # Assicuriamo siano presenti userId e bleMac
        current_config["userId"] = self._user_id
        current_config["bleMac"] = target_mac
        
        # 3. Invia la configurazione completa
        response = await self._request(API_DEVICE_SET, data=current_config)
        return True

    @staticmethod
    def make_period(start: str, end: str, watts: int) -> str:
        """Crea una stringa periodo nel formato API Powafree.
        
        La potenza viene salvata ×10 rispetto al valore in W.
        Es.: 300W → "|06:00-09:00|3000|"
        """
        return f"|{start}-{end}|{watts * 10}|"

    async def set_customize_mode(
        self,
        ble_mac: str = None,
        period_detail: list = None,
    ) -> bool:
        """Imposta la Modalità 3 (Customize Mode) con fasce orarie settimanali.

        Args:
            ble_mac:       MAC del dispositivo (usa self._ble_mac se None)
            period_detail: lista di 7 liste di stringhe periodo (use make_period()).
                           Indici: 0=Dom, 1=Lun, 2=Mar, 3=Mer, 4=Gio, 5=Ven, 6=Sab.
                           Deve coprire 00:00→23:59 senza buchi, max 12 periodi/giorno.
                           Se None usa il profilo di default ottimizzato.

        Returns:
            True se l'upload è andato a buon fine.
        """
        target_mac = ble_mac or self._ble_mac
        if not target_mac:
            await self.get_devices()
            target_mac = self._ble_mac

        base_req = {"userId": self._user_id, "bleMac": target_mac}

        # Scarica config attuale per non sovrascrivere altri campi
        try:
            config = await self._request("/api/devices/setting/download", data=base_req)
        except Exception as e:
            _LOGGER.error("Errore download config per Mod.3: %s", e)
            return False

        if not isinstance(config, dict):
            _LOGGER.error("Config non valida per Mod.3: %s", config)
            return False

        # Usa il profilo di default se non specificato
        if period_detail is None:
            period_detail = self._default_period_detail()

        config["mode"] = 3
        config["periodDetail"] = period_detail
        config["userId"] = self._user_id
        config["bleMac"] = target_mac

        try:
            await self._request("/api/devices/setting/upload", data=config)
            _LOGGER.info("Modalità 3 (Customize) impostata con successo")
            return True
        except Exception as e:
            _LOGGER.error("Errore upload Mod.3: %s", e)
            return False

    def _default_period_detail(self) -> list:
        """Profilo di default ottimizzato per uso domestico italiano.

        Strategia:
        - Notte (00:00-06:30): 350W — copre carichi standby + frigorifero
        - Mattina presto (06:30-09:00): 0W — solare inizia, lascia caricare la batteria
        - Giorno (09:00-20:00): 0W — gestito da Mod.1/Mod.2 tramite automazione HA
        - Sera (20:00-23:00): 400W — consumi serali alti (TV, luci, climatizzatori)
        - Tarda sera (23:00-23:59): 250W — ramp-down verso la notte
        """
        p = self.make_period
        giorno_base = [
            p("00:00", "06:30", 350),
            p("06:30", "09:00", 0),
            p("09:00", "20:00", 0),
            p("20:00", "23:00", 400),
            p("23:00", "23:59", 250),
        ]
        # Stessa configurazione tutti i giorni (personalizzabile)
        return [giorno_base[:] for _ in range(7)]

    async def set_mode(self, mode: int, ble_mac: str = None) -> bool:
        """Imposta la modalità operativa (1=Battery, 2=Peak, 3=Customize).
        
        Per Mod.3 usa set_customize_mode() per configurare anche i periodi.
        Questo metodo imposta solo il numero di modalità senza toccare i periodi.
        """
        return await self.set_config(ble_mac or self._ble_mac, "mode", mode)
