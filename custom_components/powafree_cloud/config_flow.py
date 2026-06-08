import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PowafreeApiClient, PowafreeAuthError, PowafreeApiClientError
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    client = PowafreeApiClient(data[CONF_EMAIL], data[CONF_PASSWORD], session)

    try:
        await client.login()
        devices = await client.get_devices()
        if not devices:
            raise Exception("No devices found on this account")
    except PowafreeAuthError:
        raise ValueError("invalid_auth")
    except PowafreeApiClientError:
        raise ValueError("cannot_connect")
    except Exception as e:
        _LOGGER.error("Unknown error: %s", e)
        raise ValueError("unknown")

    # Ritorna il titolo dell'integrazione, solitamente la mail
    return {"title": data[CONF_EMAIL]}

class PowafreeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Powafree H4."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except ValueError as err:
                errors["base"] = str(err)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
