from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Powafree sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        PowafreeSensor(coordinator, "totalSoc", "SOC", "%", SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pvTotalPower", "Potenza Solare Totale", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "pv1W", "Potenza Solare PV1", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "pv2W", "Potenza Solare PV2", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "dailyGeneration", "Generazione Giornaliera", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, scale=0.001),
        PowafreeSensor(coordinator, "maxTemperature", "Temperatura Max", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "totalSoh", "Stato di Salute (SOH)", "%", None, SensorStateClass.MEASUREMENT, scale=0.1)
    ]
    
    async_add_entities(sensors)

class PowafreeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Powafree Sensor."""

    def __init__(self, coordinator, data_key, name, unit, device_class, state_class, scale=1.0):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Powafree H4 {name}"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._scale = scale

    @property
    def native_value(self):
        """Return the state of the sensor."""
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
                return round(float(val) * self._scale, 2)
            except ValueError:
                return val
        return None

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
