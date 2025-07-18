from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import async_get_current_platform


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the sensor platform from a config entry."""
    # 直接添加实体
    async_add_entities([HelloStateSensor(hass, entry.data)])


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform (legacy YAML support)."""
    async_add_entities([HelloStateSensor(hass, config)])


class HelloStateSensor(Entity):
    """Representation of a Hello State sensor."""

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._hass = hass
        self._config = config
        self._state = None
        self._name = config.get("name", "Hello State Sensor")
        self._target_state = config.get("target_state", "hello_state.world")

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
        return f"hello_state_{self._name}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        state = self._hass.states.get(self._target_state)
        self._state = state.state if state else "Unknown"
