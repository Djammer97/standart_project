import csv
import asyncio
import httpx
import time
import os

async def post(client: httpx.AsyncClient, url, payload):
    response = await client.post(url, json=payload)
    #print(response.status_code, response.json())

async def main():
    path = os.path.join('test', 'test_data.csv')
    with open(path, encoding='utf-8') as file:
        data_list = csv.DictReader(file, delimiter=',')
        data_list = list(data_list)
    url = "http://127.0.0.1:8000/upload_data"

    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=1000, max_keepalive_connections=100), timeout=httpx.Timeout(10)) as client:
        
        start = time.time()
        tasks = [post(client, url, payload) for payload in data_list]
        await asyncio.gather(*tasks)
        end = time.time()

        print(end-start)

asyncio.run(main())