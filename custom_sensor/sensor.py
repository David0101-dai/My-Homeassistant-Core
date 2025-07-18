from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the sensor platform from a config entry."""
    async_add_entities([CustomSensor(hass, entry.data)])


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform (legacy YAML support)."""
    async_add_entities([CustomSensor(hass, config)])


class CustomSensor(SensorEntity):
    """Representation of a Custom Sensor."""

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Custom Sensor")
        self._target_state = config.get("target_state", "hello_sensor.world")
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"custom_sensor_{self._name}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        state = self._hass.states.get(self._target_state)
        self._state = state.state if state else "Unknown"
