from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def _extract(data, key):
    """Safely extract a value from coordinator data."""
    if not data or not isinstance(data, dict):
        return None
    raw = data
    if "data" in raw and isinstance(raw["data"], dict):
        raw = raw["data"]
    return raw.get(key)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Powafree sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        # ── Batteria ──
        PowafreeSensor(coordinator, "totalSoc", "SOC", "%", SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "totalSoh", "SOH", "%", None, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "batteryVoltage", "Tensione Batteria", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "batteryCurrent", "Corrente Batteria", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "batteryPower", "Potenza Batteria", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "batteryCount", "Numero Batterie", None, None, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "totalRatedCapacity", "Capacità Nominale Totale", "Wh", SensorDeviceClass.ENERGY, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "totalRemainingCapacity", "Capacità Residua Totale", "Wh", SensorDeviceClass.ENERGY, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "totalChargeEnergy", "Energia Caricata Totale", "Wh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        PowafreeSensor(coordinator, "totalChargeRemainingTime", "Tempo Rimanente Carica", "min", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "batteryWarning", "Allarme Batteria", None, None, SensorStateClass.MEASUREMENT),

        # ── Fotovoltaico ──
        PowafreeSensor(coordinator, "pvTotalPower", "Potenza Solare Totale", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pvNum", "Numero Pannelli", None, None, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "pv1W", "Potenza PV1", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv1V", "Tensione PV1", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv1A", "Corrente PV1", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv2W", "Potenza PV2", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv2V", "Tensione PV2", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv2A", "Corrente PV2", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv3W", "Potenza PV3", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv3A", "Corrente PV3", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv4W", "Potenza PV4", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv4V", "Tensione PV4", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "pv4A", "Corrente PV4", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),

        # ── Rete Elettrica (Grid) ──
        PowafreeSensor(coordinator, "gridVoltage", "Tensione Rete", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "gridCurrent", "Corrente Rete", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "gridFrequency", "Frequenza Rete", "Hz", SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT, scale=0.01),
        PowafreeSensor(coordinator, "gridCountdown", "Countdown Rete", "s", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),

        # ── Inverter ──
        PowafreeSensor(coordinator, "inverterVoltage", "Tensione Inverter", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "inverterCurrent", "Corrente Inverter", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "inverterFrequency", "Frequenza Inverter", "Hz", SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT, scale=0.01),
        PowafreeSensor(coordinator, "inverterStatus", "Stato Inverter", None, None, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "inverterModel", "Modello Inverter", None, None, None),
        PowafreeSensor(coordinator, "inverterAlert", "Allarme Inverter", None, None, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "inverterTempMax", "Temp Max Inverter", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "inverterTempMin", "Temp Min Inverter", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),

        # ── Potenze ──
        PowafreeSensor(coordinator, "activePower", "Potenza Attiva", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "apparentPower", "Potenza Apparente", "VA", SensorDeviceClass.APPARENT_POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "reactivePower", "Potenza Reattiva", "var", SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "powerFactor", "Fattore di Potenza", None, SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, scale=0.01),
        PowafreeSensor(coordinator, "power", "Potenza Totale", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "totalHeatPower", "Potenza Termica Totale", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "voltage", "Tensione", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "current", "Corrente", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "leakageCurrent", "Corrente di Dispersione", "mA", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),

        # ── Temperature ──
        PowafreeSensor(coordinator, "maxTemperature", "Temperatura Max", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "minTemperature", "Temperatura Min", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "tempMax", "Temp Max (Ambiente)", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),
        PowafreeSensor(coordinator, "tempMin", "Temp Min (Ambiente)", "°C", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, scale=0.1),

        # ── Energia ──
        PowafreeSensor(coordinator, "dailyGeneration", "Generazione Giornaliera", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, scale=0.001),
        PowafreeSensor(coordinator, "totalGeneration", "Generazione Totale", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, scale=0.001),
        PowafreeSensor(coordinator, "dailyInputEnergy", "Energia Ingresso Giornaliera", "Wh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        PowafreeSensor(coordinator, "dailyOutputEnergy", "Energia Uscita Giornaliera", "Wh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        PowafreeSensor(coordinator, "totalInputEnergy", "Energia Ingresso Totale", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, scale=0.001),
        PowafreeSensor(coordinator, "totalOutputEnergy", "Energia Uscita Totale", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, scale=0.001),
        PowafreeSensor(coordinator, "dailyCo2Savings", "Risparmio CO2 Giornaliero", "g", None, SensorStateClass.TOTAL_INCREASING),

        # ── Statistiche ──
        PowafreeSensor(coordinator, "dailyRuntime", "Tempo Funzionamento Giornaliero", "min", SensorDeviceClass.DURATION, SensorStateClass.TOTAL_INCREASING),
        PowafreeSensor(coordinator, "totalRuntime", "Tempo Funzionamento Totale", "min", SensorDeviceClass.DURATION, SensorStateClass.TOTAL_INCREASING),
        PowafreeSensor(coordinator, "Status", "Stato Dispositivo", None, None, None),
        PowafreeSensor(coordinator, "deviceAlert", "Allarme Dispositivo", None, None, SensorStateClass.MEASUREMENT),
        PowafreeSensor(coordinator, "ctRssi", "CT RSSI", "dBm", SensorDeviceClass.SIGNAL_STRENGTH, SensorStateClass.MEASUREMENT),
    ]

    # ── Sensori Config (da setting/download) ──
    config_sensors = [
        PowafreeConfigSensor(coordinator, "mode", "Modalità Operativa", None, None, None),
        PowafreeConfigSensor(coordinator, "gridCode", "Codice Rete", None, None, None),
        PowafreeConfigSensor(coordinator, "gridEnable", "Stato Immissione Rete", None, None, None),
        PowafreeConfigSensor(coordinator, "gridControl", "Controllo Rete", None, None, None),
        PowafreeConfigSensor(coordinator, "gridTime", "Tempo Rete", "s", None, None),
        PowafreeConfigSensor(coordinator, "deviceControl", "Controllo Dispositivo", None, None, None),
        PowafreeConfigSensor(coordinator, "ctEnable", "Stato CT/Meter", None, None, None),
        PowafreeConfigSensor(coordinator, "ctTotalPower", "Potenza CT Totale", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "ctAPower", "Potenza CT Fase A", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "ctBPower", "Potenza CT Fase B", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "ctCPower", "Potenza CT Fase C", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "bmsPower", "Potenza BMS", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "pfSwitch", "Stato PF Switch", None, None, None),
        PowafreeConfigSensor(coordinator, "pfValue", "Valore Power Factor", None, None, None),
        PowafreeConfigSensor(coordinator, "soc", "Soglia SOC Config", "%", SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT),
        PowafreeConfigSensor(coordinator, "periods", "Numero Periodi", None, None, None),
        PowafreeConfigSensor(coordinator, "otaStatus", "Stato OTA", None, None, None),
        PowafreeConfigSensor(coordinator, "pricePerKwh", "Prezzo per kWh", "EUR/kWh", SensorDeviceClass.MONETARY, None),
    ]

    # ── Sensori calcolati (derivati dai dati raw) ──
    computed_sensors = [
        PowafreeComputedSolarSensor(coordinator),
        PowafreeComputedChargeSensor(coordinator),
        PowafreeComputedDischargeSensor(coordinator),
    ]

    async_add_entities(sensors + config_sensors + computed_sensors)


class PowafreeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Powafree Sensor (from last_data)."""

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
        val = _extract(self.coordinator.data, self._data_key)
        if val is not None:
            try:
                return round(float(val) * self._scale, 2)
            except (ValueError, TypeError):
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


class PowafreeConfigSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Powafree Config Sensor (from setting/download)."""

    def __init__(self, coordinator, data_key, name, unit, device_class, state_class, scale=1.0):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Powafree H4 {name}"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_cfg_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._scale = scale

    @property
    def native_value(self):
        """Return the state of the config sensor."""
        config = self.coordinator.config_data
        if not config or not isinstance(config, dict):
            return None
        val = config.get(self._data_key)
        if val is not None:
            try:
                return round(float(val) * self._scale, 2)
            except (ValueError, TypeError):
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


class PowafreeComputedSolarSensor(CoordinatorEntity, SensorEntity):
    """Potenza solare reale calcolata da V×I dei pannelli.

    Il sensore nativo pvTotalPower riporta a volte valori spuri (10× il reale
    o cumulati giornalieri invece di W istantanei). Questo sensore calcola la
    potenza fisica reale moltiplicando tensione per corrente di ogni stringa PV.

    Entity ID: sensor.powafree_h4_solare_vxi
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Powafree H4 Solare V×I"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_computed_solar_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:solar-power"

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None
        raw = data.get("data", data)
        try:
            v1 = float(raw.get("pv1V", 0) or 0) * 0.1
            i1 = float(raw.get("pv1A", 0) or 0) * 0.1
            v2 = float(raw.get("pv2V", 0) or 0) * 0.1
            i2 = float(raw.get("pv2A", 0) or 0) * 0.1
            return round(v1 * i1 + v2 * i2, 1)
        except (TypeError, ValueError):
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.client._ble_mac)},
            "name": "Powafree H4",
            "manufacturer": "BigBlue",
            "model": "POWAFREE H4",
        }


class PowafreeComputedChargeSensor(CoordinatorEntity, SensorEntity):
    """Potenza di carica batteria in W (positiva quando si carica).

    Derivata da batteryPower raw con scale 0.1.
    Mostra solo i valori positivi (carica); 0 quando la batteria si scarica.

    Entity ID: sensor.powafree_h4_carica_w
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Powafree H4 Carica W"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_computed_charge_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:battery-charging"

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None
        raw = data.get("data", data)
        try:
            power = float(raw.get("batteryPower", 0) or 0) * 0.1
            # Positivo = carica, negativo = scarica
            return round(max(power, 0), 1)
        except (TypeError, ValueError):
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.client._ble_mac)},
            "name": "Powafree H4",
            "manufacturer": "BigBlue",
            "model": "POWAFREE H4",
        }


class PowafreeComputedDischargeSensor(CoordinatorEntity, SensorEntity):
    """Potenza di scarica batteria in W (positiva quando si scarica).

    Derivata da batteryPower raw con scale 0.1.
    Mostra il valore assoluto dei valori negativi; 0 quando si carica.

    Entity ID: sensor.powafree_h4_scarica_w
    """

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Powafree H4 Scarica W"
        self._attr_unique_id = f"{coordinator.client._ble_mac}_computed_discharge_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:battery-arrow-down"

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None
        raw = data.get("data", data)
        try:
            power = float(raw.get("batteryPower", 0) or 0) * 0.1
            # Negativo = scarica, positivo = carica
            return round(max(-power, 0), 1)
        except (TypeError, ValueError):
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.client._ble_mac)},
            "name": "Powafree H4",
            "manufacturer": "BigBlue",
            "model": "POWAFREE H4",
        }
