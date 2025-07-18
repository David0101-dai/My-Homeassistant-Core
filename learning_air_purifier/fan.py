from homeassistant.components.fan import FanEntity, FanEntityFeature
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
    """Set up the fan platform."""
    try:
        _LOGGER.debug("Setting up Learning Air Purifier with data: %s", entry.data)
        name = entry.data.get("name", "Learning Air Purifier")
        async_add_entities(
            [LearningAirPurifier(hass, entry.entry_id, {"name": name})],
            update_before_add=True,
        )
    except Exception as e:
        _LOGGER.error("Setup failed: %s", str(e))


class LearningAirPurifier(FanEntity):
    """A learning example of an air purifier with simulated data."""

    def __init__(self, hass, entry_id, config):
        """Initialize the air purifier."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Learning Air Purifier")
        self._is_on = False  # 初始状态：关闭
        self._speed = "off"  # 风速：off, low, medium, high
        self._air_quality = 85  # 空气质量百分比（0-100，100为最佳）
        self._filter_life = 80  # 滤芯寿命百分比（0-100，0为需更换）
        self._attr_name = self._name
        self._attr_unique_id = f"learning_air_{entry_id}"  # 使用 entry_id 确保唯一性
        self.entity_id = (
            f"fan.{self._name.lower().replace(' ', '_')}"  # 显式设置 entity_id
        )
        _LOGGER.debug(
            "Initialized Learning Air Purifier: %s with entity_id %s",
            self._name,
            self.entity_id,
        )

    @property
    def is_on(self):
        """Return True if the fan is on."""
        return self._is_on

    @property
    def speed(self):
        """Return the current speed."""
        return self._speed

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {"air_quality": self._air_quality, "filter_life": self._filter_life}

    @property
    def speed_list(self):
        """Return the list of available speeds."""
        return ["off", "low", "medium", "high"]

    @property
    def supported_features(self):
        """Return the supported features."""
        return (
            FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
            | FanEntityFeature.SET_SPEED
        )

    async def async_turn_on(
        self, speed=None, percentage=None, preset_mode=None, **kwargs
    ):
        """Turn the air purifier on with optional parameters."""
        self._is_on = True
        if speed in self.speed_list and speed != "off":
            self._speed = speed
        elif percentage is not None:
            # 转换为近似风速（简单映射，0-25%低，25-75%中，75-100%高）
            if 0 <= percentage <= 25:
                self._speed = "low"
            elif 25 < percentage <= 75:
                self._speed = "medium"
            elif percentage > 75:
                self._speed = "high"
        else:
            self._speed = "low"  # 默认低速
        _LOGGER.debug("Turned on %s with speed %s", self._name, self._speed)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the air purifier off."""
        self._is_on = False
        self._speed = "off"
        _LOGGER.debug("Turned off %s", self._name)
        self.async_write_ha_state()

    async def async_set_speed(self, speed):
        """Set the speed of the air purifier."""
        if self._is_on and speed in self.speed_list:
            self._speed = speed
            _LOGGER.debug("Set %s speed to %s", self._name, self._speed)
            self.async_write_ha_state()

    async def async_set_percentage(self, percentage):
        """Set the speed based on percentage."""
        if self._is_on and 0 <= percentage <= 100:
            if 0 <= percentage <= 25:
                self._speed = "low"
            elif 25 < percentage <= 75:
                self._speed = "medium"
            elif percentage > 75:
                self._speed = "high"
            _LOGGER.debug(
                "Set %s percentage to %s%%, mapped to speed %s",
                self._name,
                percentage,
                self._speed,
            )
            self.async_write_ha_state()

    async def async_update(self):
        """Update the air purifier state via simulated interface."""
        try:
            if self._is_on:
                # 模拟空气质量变化（-3 到 +3）
                self._air_quality += random.randint(-3, 3)
                self._air_quality = max(0, min(100, self._air_quality))
                # 模拟滤芯寿命减少（-1 到 0）
                self._filter_life += random.randint(-1, 0)
                self._filter_life = max(0, min(100, self._filter_life))
                _LOGGER.debug(
                    "Updated %s: Air Quality %s%%, Filter Life %s%%",
                    self._name,
                    self._air_quality,
                    self._filter_life,
                )
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))
