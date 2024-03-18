from aiohttp import ClientSession
import asyncio
from time import sleep

class PEC:
    """Instance of Pico Environment Control setup"""

    def __init__(self, host) -> None:
        self.host = host
        self.base_url = "http://" + self.host + "/api"
        self.mac_address = asyncio.run(self.async_populate_mac_address())

    async def async_get_api_with_response(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    return text
                else:
                    return -1
                
    async def async_put_api_with_response(self, url, data):
        async with ClientSession() as session:
            async with session.put(url, json=data) as response:
                if response.status == 200:
                    text = await response.text()
                    return text
                else:
                    return -1
    
    async def async_change_light_state(self, state: str) -> int:
        url = "http://" + self.host + "/api/light/state"
        data = {"state": state}
        async with ClientSession() as session:
            async with session.put(url, json=data) as response:
                if response.status == 200:
                    return 0
                else:
                    return -1

    async def async_get_light_state(self) -> bool:
        url = "http://" + self.host + "/api/light/state"
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    tf = await response.text()
                    if tf == "true":
                        state = True
                    else:
                        state = False
                    return state
                else:
                    print(
                        f"Failed to get the light state. Status code: {response.status_code}"
                    )
                    return ""
    
    async def async_get_brightness_pc(self) -> int:
        url = self.base_url + "/light/brightness"
        brightness = await self.async_get_api_with_response(url)
        return brightness

    async def async_set_brightness_pc(self, brightness: int) -> int:
        url = self.base_url + "/light/brightness"
        data = {"value": brightness}
        result = await self.async_put_api_with_response(url, data)
        return result

    async def async_populate_mac_address(self) -> str:
        url = self.base_url + "/wlan/mac"
        mac = await self.async_get_api_with_response(url)
        return mac
    
    def get_mac_address(self) -> str:
        return self.mac_address

# Example usage
# if __name__ == "__main__":
#     pec = PEC("192.168.13.121")

#     print(asyncio.run(pec.async_change_light_state("on")))
#     print(asyncio.run(pec.async_get_light_state()))
#     sleep(2)
#     print(asyncio.run(pec.async_change_light_state("off")))
#     print(asyncio.run(pec.async_get_light_state()))
#     sleep(2)
#     print(asyncio.run(pec.async_change_light_state("auto")))
#     print(asyncio.run(pec.async_get_light_state()))
