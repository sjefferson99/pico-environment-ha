import logging
from .pec import PEC
import voluptuous as vol
from pprint import pformat
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    SUPPORT_BRIGHTNESS,
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    LightEntity,
)
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

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
    """Representation of Pico Environment Control instance"""

    def __init__(self, light) -> None:
        _LOGGER.info(pformat(light))
        self._light = PEC(light["ip"])
        self._name = light["name"]
        self._state = None
        self._brightness = None
        self._mac_address = self._light.get_mac_address()

    @property
    def name(self) -> str:
        """Return the display name of this light"""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light"""
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
            pass  # TODO add brightness to API wrapper

        return await self._light.async_change_light_state("on")

    async def async_turn_off(self, **kwargs) -> None:
        return await self._light.async_change_light_state("off")

    async def async_update(self) -> None:
        self._state = await self._light.async_get_light_state()
        self._brightness = 255  # TODO add brightness to api library
