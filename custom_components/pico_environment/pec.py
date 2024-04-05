from aiohttp import ClientSession  # noqa: D100

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
        self.lights = [Light(f"{self._id}_light_1", f"{self._name} Light 1", self)]
        self.environment_sensors = [
            Environment_Sensor(f"{self._id}sensor_1", f"{self._name} Sensor 1", self)
        ]
        self.outdoor_humidity = Outdoor_Humidity(
            f"{self._id}outdoor_h_1", f"{self._name} Outdoor Humidity 1", self
        )

    async def async_get_api_with_response(self, url):
        """Async GET from API. Helper function for async GET requests to APIs."""
        async with ClientSession() as session, session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return text
            return -1

    async def async_put_api_with_response(self, url, data):
        """Async PUT to API. Helper function for async PUT requests to APIs."""
        async with ClientSession() as session, session.put(url, json=data) as response:
            if response.status == 200:
                text = await response.text()
                return text
            return -1

    async def async_populate_mac_address(self) -> str:
        """Query MAC from device API and populate cached value in class."""
        url = self._base_url + "/wlan/mac"
        mac = await self.async_get_api_with_response(url)
        return mac

    def get_mac_address(self) -> str:
        """Return cached MAC address value."""
        return self._mac_address

    async def test_connection(self) -> bool:
        """Test connection to API is returning sensible values. Queries MAC address and looks for ':'."""
        mac = await self.async_populate_mac_address()
        return ":" in mac


class Environment_Sensor:
    """PEC environment sensor class for measuring environmental conditions directly."""

    def __init__(self, env_id: str, name: str, controller: PEC) -> None:
        "Init an environment sensor such as humidity or temperature."
        self._id = env_id
        self._pec: PEC = controller
        self.name = name
        self._base_url = controller._base_url

    @property
    def environment_sensor_id(self) -> str:
        """Return ID for environment sensor."""
        return self._id

    async def async_update_humidity(self) -> int:
        """Query current humidity value from API."""
        url = self._base_url + "/fan/indoor_humidity"
        humidity = await self._pec.async_get_api_with_response(url)
        return humidity


class Outdoor_Humidity:
    """PEC outdoor humidity sensor class for returning local outdoor humidity conditions via the open meteo API."""

    def __init__(self, oh_id: str, name: str, controller: PEC) -> None:
        """Init an instance of a query response from open meteo for local area humidity."""
        self._id = oh_id
        self._pec = controller
        self.name = name

    @property
    def outdoor_humidity_id(self) -> str:
        """Return ID for outdoor humidity."""
        return self._id


class Light:
    """PEC light class for managing dimmable LED strips."""

    def __init__(self, light_id: str, name: str, controller: PEC) -> None:
        """Init an instance of a light or LED strip."""
        self._id = light_id
        self._pec = controller
        self.name = name
        self._base_url = self._pec._base_url

    @property
    def light_id(self) -> str:
        """Return ID for light."""
        return self._id

    async def async_change_light_state(self, state: str) -> int:
        """Update the light state On or OFF via ther device API."""
        url = self._base_url + "/light/state"
        data = {"state": state}
        result = await self._pec.async_put_api_with_response(url, data)
        return result

    async def async_get_light_state(self) -> bool:
        """Get the current light state On (True) or OFF (False) from the API."""
        url = self._base_url + "/light/state"
        tf = await self._pec.async_get_api_with_response(url)
        if tf == "true":
            return True
        return False

    async def async_get_brightness_pc(self) -> int:
        """Get the current light brightness % (0-100) from the API."""
        url = self._base_url + "/light/brightness"
        brightness = await self._pec.async_get_api_with_response(url)
        return brightness

    async def async_set_brightness_pc(self, brightness: int) -> int:
        """Set the light brightness in % (0-100) via the API."""
        url = self._base_url + "/light/brightness"
        data = {"value": brightness}
        result = await self._pec.async_put_api_with_response(url, data)
        return result
