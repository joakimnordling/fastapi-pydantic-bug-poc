import importlib.util
from pathlib import Path

from fastapi import FastAPI

from pydantic_poc.fastapi_stuff import get_fake_openapi


def main():
    poc_dir = Path(__file__).parent.relative_to(Path.cwd())
    p = (poc_dir / "models.py").absolute()
    spec = importlib.util.spec_from_file_location(name=str(p), location=str(p))

    if not spec.loader:
        raise RuntimeError(f"Failed to import {p} module")

    module = spec.loader.load_module(str(p))

    CurrentAirQualityResponse = getattr(module, "CurrentAirQualityResponse")
    CurrentAirQualityRequest = getattr(module, "CurrentAirQualityRequest")

    # print(json.dumps(CurrentAirQualityRequest.model_json_schema(), indent=2))

    app = FastAPI(
        title="Air Quality Index",
        description="Data Product for current air quality index",
        version="1.0.0",
    )

    def mock_openapi():
        data = get_fake_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            summary=app.summary,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            webhooks=app.webhooks.routes,
            tags=app.openapi_tags,
            servers=app.servers,
            separate_input_output_schemas=app.separate_input_output_schemas,
        )
        return data

    app.openapi = mock_openapi

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

    app.openapi()
    # print(json.dumps(openapi, indent=2))


if __name__ == "__main__":
    main()
