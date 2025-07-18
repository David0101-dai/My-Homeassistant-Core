from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "learning_ac"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["climate"])
    return True
