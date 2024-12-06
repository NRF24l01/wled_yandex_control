from requests import get, post
from time import sleep
import math

def color_temp_to_rgb(kelvin):
    # Clamp the color temperature to the range [1000, 40000] to avoid extreme results
    kelvin = max(1000, min(kelvin, 40000))

    # Calculate the red channel
    if kelvin <= 6600:
        red = 255
    else:
        red = 329.698727446 * ((kelvin / 100) - 60) ** -0.1332047592
        red = min(max(red, 0), 255)

    # Calculate the green channel
    if kelvin <= 6600:
        green = 99.4708025861 * ((kelvin / 100) - 10) ** 0.0755147798
        green = min(max(green, 0), 255)
    else:
        green = 288.1221695283 * ((kelvin / 100) - 60) ** -0.0755147798
        green = min(max(green, 0), 255)

    # Calculate the blue channel
    if kelvin >= 6600:
        blue = 255
    else:
        if kelvin <= 1900:
            blue = 0
        else:
            blue = 138.5177312231 * math.log(kelvin / 100 - 10) - 305.0447927307
        blue = min(max(blue, 0), 255)

    return int(red), int(green), int(blue)



class Wled_Controler:
    def __init__(self, host: str):
        self.host = "http://" + host
        return
    
    @staticmethod
    def color_temp_to_rgb(kelvin):
        kelvin = max(1000, min(kelvin, 40000))

        if kelvin <= 6600:
            red = 255
        else:
            red = 329.698727446 * ((kelvin / 100) - 60) ** -0.1332047592
            red = min(max(red, 0), 255)

        if kelvin <= 6600:
            green = 99.4708025861 * ((kelvin / 100) - 10) ** 0.0755147798
            green = min(max(green, 0), 255)
        else:
            green = 288.1221695283 * ((kelvin / 100) - 60) ** -0.0755147798
            green = min(max(green, 0), 255)

        if kelvin >= 6600:
            blue = 255
        else:
            if kelvin <= 1900:
                blue = 0
            else:
                blue = 138.5177312231 * math.log(kelvin / 100 - 10) - 305.0447927307
            blue = min(max(blue, 0), 255)

        return round(red), round(green), round(blue)
    
    @staticmethod
    def rgb_to_color_temp(r, g, b):
        rgb_2700 = (255, 180, 107)  # Warm yellowish color
        rgb_6500 = (170, 190, 255)  # Cool bluish color

        def normalize(value, min_val, max_val):
            return (value - min_val) / (max_val - min_val)

        dist_r = normalize(r, rgb_2700[0], rgb_6500[0])
        dist_g = normalize(g, rgb_2700[1], rgb_6500[1])
        dist_b = normalize(b, rgb_2700[2], rgb_6500[2])

        normalized_temp = (dist_r + dist_g + dist_b) / 3

        temp_k = 2700 + normalized_temp * (6500 - 2700)

        return max(2700, min(6500, temp_k))


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
    
    def get_color_temp(self):
        r, g, b= self._get_params()["seg"][0]["col"][0]
        return Wled_Controler.rgb_to_color_temp(r, g, b)


if __name__ == "__main__":
    wled = Wled_Controler("wled.local")
    r, g, b = color_temp_to_rgb(6500)
    print(r, g, b)
    