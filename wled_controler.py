from requests import get, post
from time import sleep
import math

def kelvin_to_rgb(kelvin):
    """
    Convert a color temperature in Kelvins to an RGB color value (0-255).

    Args:
        kelvin (float): Color temperature in Kelvins.

    Returns:
        tuple: (R, G, B) as integers in the range 0-255.
    """
    temperature = kelvin / 100

    # Calculate red
    if temperature <= 66:
        red = 255
    else:
        red = temperature - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = max(0, min(255, red))

    # Calculate green
    if temperature <= 66:
        green = temperature
        green = 99.4708025861 * (math.log(green)) - 161.1195681661
    else:
        green = temperature - 60
        green = 288.1221695283 * (green ** -0.0755148492)
    green = max(0, min(255, green))

    # Calculate blue
    if temperature >= 66:
        blue = 255
    elif temperature <= 19:
        blue = 0
    else:
        blue = temperature - 10
        blue = 138.5177312231 * (math.log(blue)) - 305.0447927307
        blue = max(0, min(255, blue))

    return int(red), int(green), int(blue)


class Wled_Controler:
    def __init__(self, host: str):
        self.host = "http://" + host
        return
    
    @staticmethod
    def color_temp_to_rgb(temp_k):
        """
        Convert a color temperature in Kelvin (2700K to 6500K) to an RGB tuple (0-255).

        Parameters:
        temp_k (float): The color temperature in Kelvin. Should be in the range 2700K-6500K.

        Returns:
        tuple: An (R, G, B) tuple with values in the range 0-255.
        """
        if temp_k < 2700:
            temp_k = 2700
        elif temp_k > 6500:
            temp_k = 6500

        # Scale the temperature to a 0-1 range
        normalized_temp = (temp_k - 2700) / (6500 - 2700)

        # Interpolate between yellowish (2700K) and bluish (6500K) colors
        # Approximate RGB values for 2700K and 6500K
        rgb_2700 = (255, 180, 107)  # Warm yellowish color
        rgb_6500 = (170, 190, 255)  # Cool bluish color

        # Interpolating each RGB component
        r = int(rgb_2700[0] + normalized_temp * (rgb_6500[0] - rgb_2700[0]))
        g = int(rgb_2700[1] + normalized_temp * (rgb_6500[1] - rgb_2700[1]))
        b = int(rgb_2700[2] + normalized_temp * (rgb_6500[2] - rgb_2700[2]))

        return r, g, b


    def _set_param(self, body: dict):
        req = post(self.host + "/json/state", json=body)
        return req.status_code == 200
    
    def _get_params(self):
        req = get(self.host+"/json/state")
        return req.json()

    def set_brightnes(self, brightnes: int):
        return self._set_param({"bri": round(brightnes / 100 * 255)})

    def set_power(self, power: bool):
        return self._set_param({"on": power})

    def get_power(self) -> bool:
        return self._get_params()["on"]
    
    def get_bri(self) -> bool:
        return round(self._get_params()["bri"] / 255 * 100)

    def enable(self):
        return self.set_power(True)

    def disable(self):
        return self.set_power(False)

    def set_color(self, rgb: tuple):
        self.fx_solid()
        return self._set_param({"seg": [{"col": [[rgb[0], rgb[1], rgb[2]]]}]})

    def set_temp(self, temp: int):
        self.fx_solid()
        self._set_param({"seg": [{"col": None}]})
        return self._set_param({"seg": [{"cct": temp}]})
    
    def fx_next(self):
        return self._set_param({"seg": [{"fx": "~"}]})
    
    def fx_prev(self):
        return self._set_param({"seg": [{"fx": "~-"}]})
    
    def fx_solid(self):
        return self._set_param({"seg": [{"fx": "-~"}]})
    
    @staticmethod
    def rgb_to_32bit(r, g, b):
        return (r << 16) | (g << 8) | b
    
    def return_32bit_color(self):
        r, g, b = self._get_params()["seg"][0]["col"][0]
        return Wled_Controler.rgb_to_32bit(r, g, b)


if __name__ == "__main__":
    wled = Wled_Controler("wled.local")
    rq = Wled_Controler.color_temp_to_rgb(2700)
    print(rq)
    