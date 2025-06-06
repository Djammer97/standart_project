from fastapi import FastAPI

from service.application.models import ModelData

import catboost
import asyncio
import os

from concurrent.futures import ThreadPoolExecutor

from service.application.pick_regno import pick_regno

app = FastAPI()
model = catboost.CatBoostClassifier()
path = os.path.join('service', 'micromodel.cbm')
model.load_model(path)

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