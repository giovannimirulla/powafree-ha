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
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Raccogliamo i dati. Nel cloud script è "last_data"
            data = await self.client.get_last_data()
            return data
        except PowafreeApiClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unknown error: {err}")
