from homeassistant.components.light import (  # noqa: D100
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .pec import PEC, Light


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Add lights for passed config_entry in HA."""
    pec: PEC = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    for light in pec.lights:
        new_entities.append(PECLight(light))  # noqa: PERF401
    if new_entities:
        async_add_entities(new_entities, update_before_add=True)


class PECLight(LightEntity):
    """Representation of Pico Environment Control instance."""

    def __init__(self, light: Light) -> None:
        """Init a PECLight."""
        self._light = light
        self._id = light.light_id
        self._name = light.name
        self._state = None
        self._brightness = None
        self._attr_unique_id = f"{self._id}"
        self._attr_name = f"{self._name}"
        self._online = False

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._id)},
            "name": f"{self._name}",
        }

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._online

    @property
    def supported_color_modes(self) -> set:
        """Return the set of supported color modes."""
        return {ColorMode.BRIGHTNESS}

    @property
    def color_mode(self) -> str:
        """Return the current color mode of the light."""
        return ColorMode.BRIGHTNESS

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light."""
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Returns boolean for light state."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        if ATTR_BRIGHTNESS in kwargs:
            brightness_value = kwargs[ATTR_BRIGHTNESS]
            brightness_pc = int(brightness_value / 2.55)
            await self._light.async_set_brightness_pc(brightness_pc)

        return await self._light.async_change_light_state("on")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        return await self._light.async_change_light_state("off")

    async def async_update(self) -> None:
        """Make API calls to the device to cache values for HA UI polls."""
        self._state = await self._light.async_get_light_state()
        self._brightness = int(int(await self._light.async_get_brightness_pc()) * 2.55)
        self._online = await self._light.async_test_light_online()
