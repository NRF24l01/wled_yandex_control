from fastapi import FastAPI, Request

from wled_controler import Wled_Controler

from config import WLED_HOST

app = FastAPI()
wled = Wled_Controler(host=WLED_HOST)

@app.get("/power")
async def power(value: bool):
    value = bool(value)
    wled.set_power(value)
    return {"value": "Ok"}

@app.get("/power/status")
async def power_status():
    return {"value": wled.get_power()}


@app.get("/bri/status")
async def bri_status():
    return {"value": str(wled.get_bri())}

@app.get("/bri")
async def bri_set(value):
    wled.set_brightnes(int(value))
    return {"value": "Ok"}


@app.get("/color")
async def set_color(r, g, b, value):
    wled.set_color((r, g, b))
    return {"value": "ok"}

@app.get("/color/status")
async def color_status():
    return {"value": wled.return_32bit_color()}


# 2700 -> 6500
@app.get("/color_temp")
async def set_color_temp(value: int):
    r, g, b = Wled_Controler.color_temp_to_rgb(value)
    wled.set_color((r, g, b))
    return {"value": {"ok"}}

@app.get("/color_temp/status")
async def get_color_temp():
    return wled.get_color_temp()


@app.get("/effects/next")
async def effect_next():
    return wled.fx_next()


@app.get("/effects/prev")
async def effect_prev():
    return wled.fx_prev()
