from fastapi import FastAPI

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
