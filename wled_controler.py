from requests import get, post
from time import sleep


class Wled_Controler:
    def __init__(self, host: str):
        self.host = "http://" + host

    def _set_param(self, body: dict):
        req = post(self.host + "/json/state", json=body)
        return req.status_code == 200

    def set_brightnes(self, brightnes: int):
        return self._set_param({"bri": round(brightnes / 255 * 100)})

    def _set_power(self, power: bool):
        return self._set_param({"on": power})

    def enable(self):
        return self._set_power(True)

    def disable(self):
        return self._set_power(False)

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


if __name__ == "__main__":
    wled = Wled_Controler("wled.local")
    rq = wled.set_temp(20)
    print(rq)
    