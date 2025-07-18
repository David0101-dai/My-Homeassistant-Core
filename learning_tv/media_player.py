from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature
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
    """Set up the media player platform."""
    try:
        _LOGGER.debug("Setting up Learning TV with data: %s", entry.data)
        name = entry.data.get("name", "Learning TV")
        async_add_entities([LearningTv(hass, {"name": name})], update_before_add=True)
    except Exception as e:
        _LOGGER.error("Setup failed: %s", str(e))


class LearningTv(MediaPlayerEntity):
    """A learning example of a TV with simulated data."""

    def __init__(self, hass, config):
        """Initialize the TV."""
        self._hass = hass
        self._config = config
        self._name = config.get("name", "Learning TV")
        self._state = "off"  # 状态：off, playing, paused
        self._volume_level = 0.5  # 音量（0.0 到 1.0）
        self._media_title = "Channel 1"  # 当前播放内容
        self._channel_list = [f"Channel {i}" for i in range(1, 11)]  # 频道列表
        self._current_channel_index = 0  # 当前频道索引
        self._attr_name = self._name
        self._attr_unique_id = f"learning_tv_{self._name}"
        _LOGGER.debug("Initialized Learning TV: %s", self._name)

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @property
    def volume_level(self):
        """Return the volume level."""
        return self._volume_level

    @property
    def media_title(self):
        """Return the current media title."""
        return self._media_title

    @property
    def supported_features(self):
        """Return the supported features based on current state."""
        features = (
            MediaPlayerEntityFeature.VOLUME_SET
            | MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
        )
        if self._state == "playing":
            features |= MediaPlayerEntityFeature.PAUSE
        elif self._state == "paused":
            features |= MediaPlayerEntityFeature.PLAY
        return features

    async def async_turn_on(self):
        """Turn the TV on."""
        self._state = "playing"
        _LOGGER.debug("Turned on %s", self._name)
        self.async_write_ha_state()  # 直接写入状态，避免触发频道更新

    async def async_turn_off(self):
        """Turn the TV off."""
        self._state = "off"
        _LOGGER.debug("Turned off %s", self._name)
        self.async_write_ha_state()  # 直接写入状态

    async def async_set_volume_level(self, volume):
        """Set the volume level (0.0 to 1.0)."""
        if 0 <= volume <= 1:
            self._volume_level = volume
            _LOGGER.debug("Set volume for %s to %s", self._name, self._volume_level)
            self.async_write_ha_state()  # 直接写入状态，避免触发频道更新

    async def async_media_play(self):
        """Start or resume playback."""
        if self._state in ["off", "paused"]:
            self._state = "playing"
            _LOGGER.debug("Started playing on %s", self._name)
            self.async_write_ha_state()  # 直接写入状态

    async def async_media_pause(self):
        """Pause playback."""
        if self._state == "playing":
            self._state = "paused"
            _LOGGER.debug("Paused %s", self._name)
            self.async_write_ha_state()  # 直接写入状态，避免触发频道更新

    async def async_next_channel(self):
        """Switch to the next channel."""
        if self._state in ["playing", "paused"]:
            self._current_channel_index = (self._current_channel_index + 1) % len(
                self._channel_list
            )
            self._media_title = self._channel_list[self._current_channel_index]
            _LOGGER.debug(
                "Switched %s to next channel: %s", self._name, self._media_title
            )
            self.async_write_ha_state()  # 直接写入状态

    async def async_previous_channel(self):
        """Switch to the previous channel."""
        if self._state in ["playing", "paused"]:
            self._current_channel_index = (self._current_channel_index - 1) % len(
                self._channel_list
            )
            self._media_title = self._channel_list[self._current_channel_index]
            _LOGGER.debug(
                "Switched %s to previous channel: %s", self._name, self._media_title
            )
            self.async_write_ha_state()  # 直接写入状态

    async def async_update(self):
        """Update the TV state via simulated interface."""
        try:
            if self._state == "playing":
                # 仅在播放状态下随机切换频道
                new_index = random.randint(0, len(self._channel_list) - 1)
                if new_index != self._current_channel_index:
                    self._current_channel_index = new_index
                    self._media_title = self._channel_list[self._current_channel_index]
                    _LOGGER.debug(
                        "Updated %s media title to %s", self._name, self._media_title
                    )
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Update failed for %s: %s", self._name, str(e))
