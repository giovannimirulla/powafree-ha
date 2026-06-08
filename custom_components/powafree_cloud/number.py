import logging
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Powafree number entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Dalle stringhe DEX: "setActivePower"
    numbers = [
        PowafreeNumber(coordinator, "activePower", "Potenza Attiva Immissione", "W", 0, 800, 10)
    ]
    
    async_add_entities(numbers)

class PowafreeNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Powafree Number (Slider)."""

    def __init__(self, coordinator, data_key, name, unit, min_val, max_val, step):
        """Initialize the number."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Powafree H4 {name}"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_number_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        if not self.coordinator.data:
            return None
        
        raw_data = self.coordinator.data
        if isinstance(raw_data, dict) and "data" in raw_data and isinstance(raw_data["data"], dict):
            raw_data = raw_data["data"]
        elif not isinstance(raw_data, dict):
            raw_data = {}
            
        val = raw_data.get(self._data_key)
        
        if val is not None:
            try:
                return float(val)
            except ValueError:
                pass
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        success = await self.coordinator.client.set_config(
            self.coordinator.client._ble_mac, self._data_key, int(value)
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
