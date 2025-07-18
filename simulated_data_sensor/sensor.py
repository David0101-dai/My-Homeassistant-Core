from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
import random
from datetime import timedelta
import logging

SCAN_INTERVAL = timedelta(seconds=5)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the sensor platform from a config entry."""
    try:
        _LOGGER.debug("Setting up Simulated Data Sensor entry: %s", entry.data)
        async_add_entities(
            [SimulatedDataSensor(hass, entry.data)], update_before_add=True
        )
    except Exception as e:
        _LOGGER.error("Failed to set up sensor: %s", str(e))


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform (legacy YAML support)."""
    try:
        _LOGGER.debug("Setting up Simulated Data Sensor platform: %s", config)
        async_add_entities([SimulatedDataSensor(hass, config)], update_before_add=True)
    except Exception as e:
        _LOGGER.error("Failed to set up platform sensor: %s", str(e))


class SimulatedDataSensor(SensorEntity):
    """Representation of a sensor with simulated data."""

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Simulated Sensor")
        self._state = None
        self._attr_name = self._name
        self._attr_unique_id = f"simulated_data_sensor_{self._name}"
        self._attr_native_unit_of_measurement = "°C"
        _LOGGER.debug("Initialized SimulatedDataSensor: %s", self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch simulated data for the sensor."""
        try:
            self._state = round(random.uniform(15, 30), 1)
            _LOGGER.debug("Updated state for %s to %s", self._name, self._state)
            self.async_write_ha_state()  # 强制写入状态
        except Exception as e:
            self._state = "Error"
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))

    async def async_added_to_hass(self):
        """Run when entity is added to hass."""
        _LOGGER.debug("Entity %s added to hass", self._name)
