from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "simulated_data_sensor"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Simulated Data Sensor component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Simulated Data Sensor from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
