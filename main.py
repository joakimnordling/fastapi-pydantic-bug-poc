import importlib
from pathlib import Path

from fastapi import FastAPI

import routes

app = FastAPI(
    title="Air Quality Index",
    description="Data Product for current air quality index",
    version="1.0.0",
)
app.include_router(routes.router)


p = Path("models.py")
spec = importlib.util.spec_from_file_location(name=str(p), location=str(p))

if not spec.loader:
    raise RuntimeError(f"Failed to import {p} module")

module = spec.loader.load_module(str(p))

CurrentAirQualityResponse = getattr(module, "CurrentAirQualityResponse")
CurrentAirQualityRequest = getattr(module, "CurrentAirQualityRequest")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(
    "/AirQuality/Current",
    response_model=CurrentAirQualityResponse,
)
def read_item(data: CurrentAirQualityRequest):
    return CurrentAirQualityResponse(
        air_quality_index=30,
        timestamp="2020-04-03T13:00:00Z",
        attribution=["XYZ environmental monitoring"],
    )
