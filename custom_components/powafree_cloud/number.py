import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Powafree number entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    numbers = [
        PowafreeNumber(coordinator, "activePower", "Potenza Attiva Immissione",
                       "W", 0, 800, 10, "mdi:flash"),
        PowafreeNumber(coordinator, "bmsPower", "Potenza BMS",
                       "W", 0, 800, 10, "mdi:battery-charging"),
        PowafreeNumber(coordinator, "soc", "Soglia SOC Minimo",
                       "%", 0, 100, 1, "mdi:battery-low"),
        PowafreeNumber(coordinator, "gridCode", "Codice Rete",
                       None, 0, 100, 1, "mdi:earth"),
        PowafreeNumber(coordinator, "gridTime", "Tempo Rete",
                       "s", 0, 600, 1, "mdi:timer"),
        PowafreeNumber(coordinator, "mode", "Modalità Operativa",
                       None, 0, 10, 1, "mdi:cog"),
        PowafreeNumber(coordinator, "periods", "Numero Periodi Fasce Orarie",
                       None, 0, 10, 1, "mdi:clock-outline"),
        PowafreeNumber(coordinator, "pfValue", "Valore Power Factor",
                       None, 0, 100, 1, "mdi:sine-wave"),
        PowafreeNumber(coordinator, "ctTotalPower", "Potenza CT Totale",
                       "W", 0, 10000, 10, "mdi:meter-electric"),
        PowafreeNumber(coordinator, "ctAPower", "Potenza CT Fase A",
                       "W", 0, 10000, 10, "mdi:meter-electric"),
        PowafreeNumber(coordinator, "ctBPower", "Potenza CT Fase B",
                       "W", 0, 10000, 10, "mdi:meter-electric"),
        PowafreeNumber(coordinator, "ctCPower", "Potenza CT Fase C",
                       "W", 0, 10000, 10, "mdi:meter-electric"),
        PowafreeNumber(coordinator, "pricePerKwh", "Prezzo per kWh",
                       "EUR/kWh", 0, 1, 0.01, "mdi:currency-eur"),
    ]

    async_add_entities(numbers)


class PowafreeNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Powafree Number (config setting)."""

    def __init__(self, coordinator, data_key, name, unit, min_val, max_val, step, icon=None):
        """Initialize the number."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Powafree H4 {name}"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_number_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_mode = NumberMode.SLIDER
        if icon:
            self._attr_icon = icon

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        config = self.coordinator.config_data
        if not config or not isinstance(config, dict):
            return None
        val = config.get(self._data_key)
        if val is not None:
            try:
                return float(val)
            except (ValueError, TypeError):
                pass
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        # pricePerKwh is a float, the rest are int
        send_value = value if self._data_key == "pricePerKwh" else int(value)
        success = await self.coordinator.client.set_config(
            self.coordinator.client._ble_mac, self._data_key, send_value
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
            "manufacturer": "BigBlue",
            "model": "POWAFREE H4",
        }
