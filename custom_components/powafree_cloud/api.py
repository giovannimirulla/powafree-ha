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
                    if "token" in msg.lower() or json_data.get("code") == 401: # Adattare ai codici di errore reali
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
            # Dallo script bash sappiamo che la risposta diretta (o dentro data) ha token e userId
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
        
        # La risposta è solitamente una lista in "data"
        if isinstance(response, list):
            if response:
                # Salva il primo dispositivo di default
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
        
    async def set_config(self, ble_mac: str, key: str, value: Any) -> bool:
        """
        Send a command to the device.
        Endpoint e struttura da definire esattamente in base al reverse engineering
        delle API post cattura o tentativi futuri.
        """
        target_mac = ble_mac or self._ble_mac
        data = {
            "userId": self._user_id,
            "bleMac": target_mac,
            "config": {key: value} # Struttura ipotetica, da raffinare
        }
        
        # In assenza del path esatto, simuliamo un log per ora finché non sniffiamo l'app
        _LOGGER.warning("Comando SET non ancora implementato a livello API reale. Tentativo invio: %s=%s", key, value)
        return True # Simuliamo successo
