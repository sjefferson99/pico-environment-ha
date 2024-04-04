import asyncio  # noqa: D100

from aiohttp import ClientSession

from homeassistant.core import HomeAssistant


class PEC:
    """Setup instance of Pico Environment Control."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Configure a PEC hub instance."""
        self._host = host
        self._name = host
        self._id = host.lower()
        self._base_url = "http://" + self._host + "/api"
        self._mac_address = None
        self.lights = [Light(f"{self._id}_1", f"{self._name} 1", self)]
        self.environment_sensors = [
            Environment_Sensor(f"{self._id}_1", f"{self._name} 1", self)
        ]
        self.outdoor_humidity = Outdoor_Humidity(
            f"{self._id}_1", f"{self._name} 1", self
        )

    async def async_get_api_with_response(self, url):
        async with ClientSession() as session, session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return text
            return -1

    async def _async_put_api_with_response(self, url, data):
        async with ClientSession() as session, session.put(url, json=data) as response:
            if response.status == 200:
                text = await response.text()
                return text
            return -1

    async def async_populate_mac_address(self) -> str:
        url = self._base_url + "/wlan/mac"
        mac = await self.async_get_api_with_response(url)
        return mac

    def get_mac_address(self) -> str:
        return self._mac_address

    async def test_connection(self) -> bool:
        mac = await self.async_populate_mac_address()
        return ":" in mac


class Environment_Sensor:
    """PEC environment sensor class for measuring environmental conditions directly."""

    def __init__(self, id: str, name: str, controller: PEC) -> None:
        self._id = id
        self._pec: PEC = controller
        self.name = name
        self._base_url = controller._base_url

    @property
    def environment_sensor_id(self) -> str:
        """Return ID for environment sensor."""
        return self._id

    async def async_update_humidity(self) -> int:
        url = self._base_url + "/fan/indoor_humidity"
        humidity = await self._pec.async_get_api_with_response(url)
        return humidity


class Outdoor_Humidity:
    """PEC outdoor humidity sensor class for returning local outdoor humidity conditions via the open meteo API."""

    def __init__(self, id: str, name: str, controller: PEC) -> None:
        self._id = id
        self._pec = controller
        self.name = name

    @property
    def outdoor_humidity_id(self) -> str:
        """Return ID for outdoor humidity."""
        return self._id


class Light:
    """PEC light class for managing dimmable LED strips."""

    def __init__(self, id: str, name: str, controller: PEC) -> None:
        self._id = id
        self._pec = controller
        self.name = name
        self._base_url = self._pec._base_url

    @property
    def light_id(self) -> str:
        """Return ID for light."""
        return self._id

    async def async_change_light_state(self, state: str) -> int:
        url = self._base_url + "/light/state"
        data = {"state": state}
        result = await self._pec._async_put_api_with_response(url, data)
        return result

    async def async_get_light_state(self) -> bool:
        url = self._base_url + "/light/state"
        tf = await self._pec.async_get_api_with_response(url)
        if tf == "true":
            return True
        return False

    async def async_get_brightness_pc(self) -> int:
        url = self._base_url + "/light/brightness"
        brightness = await self._pec.async_get_api_with_response(url)
        return brightness

    async def async_set_brightness_pc(self, brightness: int) -> int:
        url = self._base_url + "/light/brightness"
        data = {"value": brightness}
        result = await self._pec._async_put_api_with_response(url, data)
        return result
