from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "custom_sensor"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Custom Sensor component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Custom Sensor from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
