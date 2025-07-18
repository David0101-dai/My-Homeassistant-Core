from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "custom_switch"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Custom Switch component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Custom Switch from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["switch"])
    return True
