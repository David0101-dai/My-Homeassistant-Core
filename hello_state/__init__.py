from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "hello_state"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Hello State component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Hello State from a config entry."""
    # 转发到 sensor 平台
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
