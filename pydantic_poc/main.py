import importlib.util
import json
from pathlib import Path

from pydantic.json_schema import models_json_schema


def import_my_model():
    """
    Import a Pydantic model using importlib from an absolute filesystem path.
    """
    poc_dir = Path(__file__).parent.relative_to(Path.cwd())
    p = (poc_dir / "models.py").absolute()
    spec = importlib.util.spec_from_file_location(name="models", location=str(p))

    if not spec.loader:
        raise RuntimeError(f"Failed to import {p} module")

    module = spec.loader.load_module(str(p))

    return getattr(module, "MyModel")


def main():
    MyModel = import_my_model()

    _, top_level_schema = models_json_schema(
        [(MyModel, "validation")], title="My Schema"
    )
    print(json.dumps(top_level_schema, indent=2))


if __name__ == "__main__":
    main()
