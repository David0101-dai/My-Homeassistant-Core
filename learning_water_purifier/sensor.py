from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import random
from datetime import timedelta
import logging

# 轮询间隔（15秒）
SCAN_INTERVAL = timedelta(seconds=15)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the sensor platform."""
    try:
        _LOGGER.debug("Setting up Learning Water Purifier with data: %s", entry.data)
        name = entry.data.get("name", "Learning Water Purifier")
        async_add_entities(
            [LearningWaterPurifier(hass, {"name": name})], update_before_add=True
        )
    except Exception as e:
        _LOGGER.error("Setup failed: %s", str(e))


class LearningWaterPurifier(SensorEntity):
    """A learning example of a water purifier with simulated data."""

    def __init__(self, hass, config):
        """Initialize the water purifier."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Learning Water Purifier")
        self._state = "off"  # 状态：off, on
        self._water_quality = 90  # 水质百分比（0-100，100为最佳）
        self._filter_life = 75  # 滤芯寿命百分比（0-100，0为需更换）
        self._mode = "normal"  # 模式：normal, turbo
        self._attr_name = self._name
        self._attr_unique_id = f"learning_water_{self._name}"
        self._attr_native_unit_of_measurement = "%"  # 单位
        _LOGGER.debug("Initialized Learning Water Purifier: %s", self._name)

    @property
    def state(self):
        """Return the state (water quality or mode, depending on context)."""
        return self._water_quality

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "mode": self._mode,
            "filter_life": self._filter_life,
            "status": self._state,
        }

    async def async_turn_on(self):
        """Turn the water purifier on."""
        self._state = "on"
        _LOGGER.debug("Turned on %s", self._name)
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn the water purifier off."""
        self._state = "off"
        _LOGGER.debug("Turned off %s", self._name)
        self.async_write_ha_state()

    async def async_set_mode(self, mode):
        """Set the operation mode."""
        if mode in ["normal", "turbo"]:
            self._mode = mode
            _LOGGER.debug("Set %s mode to %s", self._name, self._mode)
            self.async_write_ha_state()

    async def async_update(self):
        """Update the water purifier state via simulated interface."""
        try:
            if self._state == "on":
                # 模拟水质变化（-2 到 +2）
                self._water_quality += random.randint(-2, 2)
                self._water_quality = max(0, min(100, self._water_quality))
                # 模拟滤芯寿命减少（-1 到 0）
                self._filter_life += random.randint(-1, 0)
                self._filter_life = max(0, self._filter_life)
                _LOGGER.debug(
                    "Updated %s: Water Quality %s%%, Filter Life %s%%",
                    self._name,
                    self._water_quality,
                    self._filter_life,
                )
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))
