import importlib
import json
from pathlib import Path

p = Path("models.py").absolute()
spec = importlib.util.spec_from_file_location(name=str(p), location=str(p))

if not spec.loader:
    raise RuntimeError(f"Failed to import {p} module")

module = spec.loader.load_module(str(p))

CurrentAirQualityResponse = getattr(module, "CurrentAirQualityResponse")
CurrentAirQualityRequest = getattr(module, "CurrentAirQualityRequest")

print(json.dumps(CurrentAirQualityRequest.model_json_schema(), indent=2))
