import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PowafreeApiClient, PowafreeApiClientError
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PowafreeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Powafree data."""

    def __init__(self, hass: HomeAssistant, client: PowafreeApiClient) -> None:
        """Initialize."""
        self.client = client
        self.config_data: dict = {}
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API (both last_data and setting/download)."""
        try:
            # Dati telemetrici in tempo reale
            data = await self.client.get_last_data()

            # Configurazione del dispositivo (per switch e number)
            try:
                self.config_data = await self.client.get_config()
            except PowafreeApiClientError as cfg_err:
                _LOGGER.warning("Impossibile scaricare la configurazione: %s", cfg_err)
                # Non blocchiamo il polling se la config fallisce

            return data
        except PowafreeApiClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unknown error: {err}")
