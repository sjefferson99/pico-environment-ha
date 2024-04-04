"""Pico Environment Control"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import pec  # TODO I think this should be from .pec import PEC and change line 14
from .const import DOMAIN

PLATFORMS: list[str] = ["light", "sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pico Environment from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = pec.PEC(hass, entry.data["host"])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
