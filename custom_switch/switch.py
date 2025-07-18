from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.switch import SwitchEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the switch platform from a config entry."""
    async_add_entities([CustomSwitch(hass, entry.data)])


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switch platform (legacy YAML support)."""
    async_add_entities([CustomSwitch(hass, config)])


class CustomSwitch(SwitchEntity):
    """Representation of a Custom Switch."""

    def __init__(self, hass, config):
        """Initialize the switch."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Custom Switch")
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"custom_switch_{self._name}"

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._state = False
