from homeassistant.components.cover import CoverEntity, CoverEntityFeature
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
    """Set up the cover platform."""
    try:
        _LOGGER.debug("Setting up Learning Cover with data: %s", entry.data)
        name = entry.data.get("name", "Learning Cover")
        async_add_entities(
            [LearningCover(hass, {"name": name})], update_before_add=True
        )
    except Exception as e:
        _LOGGER.error("Setup failed: %s", str(e))


class LearningCover(CoverEntity):
    """A learning example of a cover with simulated data."""

    def __init__(self, hass, config):
        """Initialize the cover."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Learning Cover")
        self._is_closed = True  # 初始状态：关闭
        self._current_position = 0  # 位置（0-100%，0为完全关闭）
        self._attr_name = self._name
        self._attr_unique_id = f"learning_cover_{self._name}"
        _LOGGER.debug("Initialized Learning Cover: %s", self._name)

    @property
    def is_closed(self):
        """Return True if the cover is closed."""
        return self._is_closed

    @property
    def current_cover_position(self):
        """Return the current position of the cover (0-100%)."""
        return self._current_position

    @property
    def supported_features(self):
        """Return the supported features."""
        return (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.SET_POSITION
        )

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        self._is_closed = False
        self._current_position = 100
        _LOGGER.debug("Opened %s", self._name)
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        self._is_closed = True
        self._current_position = 0
        _LOGGER.debug("Closed %s", self._name)
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs):
        """Set the cover position (0-100%)."""
        if (position := kwargs.get("position")) is not None:
            if 0 <= position <= 100:
                self._current_position = position
                self._is_closed = position == 0
                _LOGGER.debug(
                    "Set %s position to %s%%", self._name, self._current_position
                )
                self.async_write_ha_state()

    async def async_update(self):
        """Update the cover state via simulated interface."""
        try:
            # 模拟位置随机变化（仅在非完全打开或关闭时）
            if not self._is_closed and self._current_position < 100:
                new_position = self._current_position + random.randint(-5, 5)
                self._current_position = max(0, min(100, new_position))
                self._is_closed = self._current_position == 0
                _LOGGER.debug(
                    "Updated %s position to %s%%", self._name, self._current_position
                )
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))
