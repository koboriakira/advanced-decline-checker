from fastapi import FastAPI
from advanced_decline_checker.controller import check_ratio

app = FastAPI()


@app.get('/')  # methodとendpointの指定
async def hello():
    is_success = check_ratio()
    return {"statusCode": 200 if is_success else 500}
