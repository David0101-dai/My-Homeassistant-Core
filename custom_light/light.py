from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.light import LightEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the light platform from a config entry."""
    async_add_entities([CustomLight(hass, entry.data)])


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the light platform (legacy YAML support)."""
    async_add_entities([CustomLight(hass, config)])


class CustomLight(LightEntity):
    """Representation of a Custom Light."""

    def __init__(self, hass, config):
        """Initialize the light."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Custom Light")
        self._state = False

    @property
    def name(self):
        """Return the name of the light."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the light."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"custom_light_{self._name}"

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        self._state = False
