from fastapi import FastAPI

from wled_controler import Wled_Controler

from config import WLED_HOST

app = FastAPI()
wled = Wled_Controler(host=WLED_HOST)

@app.get("/")
async def root():
    return {"message": "Hello World"}