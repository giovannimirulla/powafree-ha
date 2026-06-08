import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PowafreeApiClient
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
from .coordinator import PowafreeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "switch", "number"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Powafree from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]

    session = async_get_clientsession(hass)
    client = PowafreeApiClient(email, password, session)
    
    # Login and get devices to fetch bleMac
    try:
        await client.login()
        await client.get_devices()
    except Exception as ex:
        _LOGGER.error("Error setting up Powafree api client: %s", ex)
        return False

    coordinator = PowafreeDataUpdateCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
