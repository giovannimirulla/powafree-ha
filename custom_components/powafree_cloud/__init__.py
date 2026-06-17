import asyncio
import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import PowafreeApiClient
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
from .coordinator import PowafreeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "switch", "number"]

# Schema per il servizio set_customize_mode
SERVICE_SET_CUSTOMIZE_MODE = "set_customize_mode"
SERVICE_SCHEMA_CUSTOMIZE = vol.Schema({
    vol.Optional("periods"): list,  # lista di 7 liste (opzionale, usa default se assente)
})


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

    # ── Registra i servizi custom ──────────────────────────────────────────────

    async def handle_set_customize_mode(call: ServiceCall) -> None:
        """Imposta Mod.3 (Customize) con fasce orarie settimanali."""
        periods = call.data.get("periods")  # None = usa il profilo di default
        for coordinator in hass.data[DOMAIN].values():
            try:
                ok = await coordinator.client.set_customize_mode(period_detail=periods)
                if ok:
                    await coordinator.async_request_refresh()
                    _LOGGER.info("Modalità 3 (Customize) impostata tramite servizio HA")
                else:
                    _LOGGER.error("Impossibile impostare Modalità 3")
            except Exception as ex:
                _LOGGER.error("Errore set_customize_mode: %s", ex)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_CUSTOMIZE_MODE,
        handle_set_customize_mode,
        schema=SERVICE_SCHEMA_CUSTOMIZE,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
