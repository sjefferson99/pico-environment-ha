"""Platform for sensor integration."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .pec import PEC, Environment_Sensor


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    pec: PEC = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    for environment_sensor in pec.environment_sensors:
        new_entities.append(EnvironmentSensor(environment_sensor))
        new_entities.append(HumiditySensor(environment_sensor))
    if new_entities:
        async_add_entities(new_entities, update_before_add=True)


class EnvironmentSensor(Entity):
    """Environment sensor device class."""

    should_poll = True

    def __init__(self, environment_sensor: Environment_Sensor) -> None:
        """Init an environment sensor module (device) containing the various sensor entities."""
        self._environment_sensor = environment_sensor
        self._attr_unique_id = f"{self._environment_sensor.environment_sensor_id}"
        self._attr_name = f"{self._environment_sensor.name}"

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._environment_sensor.environment_sensor_id)},
            "name": f"{self._environment_sensor.name}",
        }


class SensorBase(Entity):
    """Base representation of a Pico Environment Sensor."""

    should_poll = True

    def __init__(self, environment_sensor: Environment_Sensor) -> None:
        """Initialize the sensor."""
        self._environment_sensor = environment_sensor
        self._online = True

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._environment_sensor.environment_sensor_id)}
        }

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._online


class HumiditySensor(SensorBase):
    """Specific humidity sensor class."""

    device_class = SensorDeviceClass.HUMIDITY

    def __init__(self, environment_sensor: Environment_Sensor) -> None:
        """Initialize the sensor."""
        super().__init__(environment_sensor)
        self._attr_unique_id = (
            f"{self._environment_sensor.environment_sensor_id}_humidity"
        )
        self._attr_name = f"{self._environment_sensor.name} Humidity"
        self._humidity = 0

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._humidity

    async def async_update(self) -> None:
        """Make API calls to the device to cache values for HA UI polls."""
        self._humidity = await self._environment_sensor.async_update_humidity()
        self._online = await self._environment_sensor.async_test_sensors_online()
