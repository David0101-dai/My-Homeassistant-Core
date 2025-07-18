from homeassistant.components.climate import ClimateEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import random
from datetime import timedelta
import logging

# 轮询间隔（10秒）
SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the climate platform."""
    try:
        _LOGGER.debug("Setting up Learning AC with data: %s", entry.data)
        name = entry.data.get("name", "Learning AC")
        async_add_entities([LearningAc(hass, {"name": name})], update_before_add=True)
    except Exception as e:
        _LOGGER.error("Setup failed: %s", str(e))


class LearningAc(ClimateEntity):
    """A learning example of an air conditioner with simulated data."""

    def __init__(self, hass, config):
        """Initialize the air conditioner."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Learning AC")
        self._current_temperature = 25.0  # 初始温度
        self._target_temperature = 22.0  # 初始目标温度
        self._hvac_mode = "cool"  # 模式：cool, heat, off
        self._fan_mode = "auto"  # 风速：auto, low, medium, high
        self._attr_name = self._name
        self._attr_unique_id = f"learning_ac_{self._name}"
        _LOGGER.debug("Initialized Learning AC: %s", self._name)

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return "°C"

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._target_temperature

    @property
    def hvac_mode(self):
        """Return the current HVAC mode."""
        return self._hvac_mode

    @property
    def fan_mode(self):
        """Return the current fan mode."""
        return self._fan_mode

    @property
    def hvac_modes(self):
        """Return a list of available HVAC modes."""
        return ["off", "cool", "heat"]

    @property
    def fan_modes(self):
        """Return a list of available fan modes."""
        return ["auto", "low", "medium", "high"]

    async def async_set_temperature(self, **kwargs):
        """Set the target temperature."""
        if (temperature := kwargs.get("temperature")) is not None:
            self._target_temperature = float(temperature)
            _LOGGER.debug(
                "Set target temperature for %s to %s °C",
                self._name,
                self._target_temperature,
            )
            await self.async_update()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode."""
        if hvac_mode in self.hvac_modes:
            self._hvac_mode = hvac_mode
            _LOGGER.debug("Set HVAC mode for %s to %s", self._name, self._hvac_mode)
            await self.async_update()

    async def async_set_fan_mode(self, fan_mode):
        """Set the fan mode."""
        if fan_mode in self.fan_modes:
            self._fan_mode = fan_mode
            _LOGGER.debug("Set fan mode for %s to %s", self._name, self._fan_mode)
            await self.async_update()

    async def async_update(self):
        """Update the air conditioner state via simulated interface."""
        try:
            if self._hvac_mode != "off":
                # 模拟温度向目标靠拢
                delta = (self._target_temperature - self._current_temperature) * 0.1
                self._current_temperature += delta
                self._current_temperature = round(self._current_temperature, 1)
            _LOGGER.debug(
                "Updated %s: Current %s °C, Target %s °C, Mode %s, Fan %s",
                self._name,
                self._current_temperature,
                self._target_temperature,
                self._hvac_mode,
                self._fan_mode,
            )
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))
