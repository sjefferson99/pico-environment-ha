import logging  # noqa: D100
from pprint import pformat

import voluptuous as vol

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .pec import PEC

_LOGGER = logging.getLogger("pec")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME): cv.string,
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    _LOGGER.info(pformat(config))

    light = {"name": config[CONF_NAME], "ip": config[CONF_IP_ADDRESS]}

    add_entities([PicoEnvironment(light)])


class PicoEnvironment(LightEntity):
    """Representation of Pico Environment Control instance."""

    def __init__(self, light) -> None:
        _LOGGER.info(pformat(light))
        self._light = PEC(light["ip"])
        self._name = light["name"]
        self._state = None
        self._brightness = None
        self._mac_address = self._light.get_mac_address()

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light."""
        return self._brightness

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._mac_address

    @property
    def is_on(self) -> bool | None:
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            brightness_value = kwargs[ATTR_BRIGHTNESS]
            brightness_pc = int(brightness_value / 2.55)
            await self._light.async_set_brightness_pc(brightness_pc)

        return await self._light.async_change_light_state("on")

    async def async_turn_off(self, **kwargs) -> None:
        return await self._light.async_change_light_state("off")

    async def async_update(self) -> None:
        self._state = await self._light.async_get_light_state()
        self._brightness = int(int(await self._light.async_get_brightness_pc()) * 2.55)
