import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Powafree switches."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Dalla stringa DEX: "setGridEnable", "setBmsEnable"
    switches = [
        PowafreeSwitch(coordinator, "gridEnable", "Immissione in Rete"),
        PowafreeSwitch(coordinator, "bmsEnable", "Abilitazione BMS")
    ]
    
    async_add_entities(switches)

class PowafreeSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Powafree Switch."""

    def __init__(self, coordinator, data_key, name):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Powafree H4 {name}"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_switch_{data_key}"

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        
        raw_data = self.coordinator.data
        if isinstance(raw_data, dict) and "data" in raw_data and isinstance(raw_data["data"], dict):
            raw_data = raw_data["data"]
        elif not isinstance(raw_data, dict):
            raw_data = {}
            
        val = raw_data.get(self._data_key)
        
        # Ipotizziamo che 1 o "1" o True sia acceso
        return val in (1, "1", True, "true", "True")

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        success = await self.coordinator.client.set_config(
            self.coordinator.client._ble_mac, self._data_key, 1
        )
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        success = await self.coordinator.client.set_config(
            self.coordinator.client._ble_mac, self._data_key, 0
        )
        if success:
            await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        """Device info for grouping."""
        mac = self.coordinator.client._ble_mac
        return {
            "identifiers": {(DOMAIN, mac)},
            "name": "Powafree H4",
            "manufacturer": "BigBlue"
        }
