from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "custom_light"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Custom Light component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Custom Light from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["light"])
    return True
