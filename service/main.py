from fastapi import FastAPI

from app.models import ModelData

import catboost
import asyncio

from concurrent.futures import ThreadPoolExecutor

from app.pick_regno import pick_regno

app = FastAPI()
model = catboost.CatBoostClassifier()
model.load_model('micromodel.cbm')

executor = ThreadPoolExecutor(max_workers=8)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/upload_data")
async def app_post_upload_data(data: ModelData):
    loop = asyncio.get_running_loop()
    features = [*await data.get_args(), model]
    result = await loop.run_in_executor(executor, pick_regno, *features)
    return {"message": result.tolist()}