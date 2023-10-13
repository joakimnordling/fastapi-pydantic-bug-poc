import json
from pathlib import Path

import main


def test_openapi_spec():
    openapi = main.app.openapi()
    out_file = Path("openapi.json")
    out_file.write_text(
        json.dumps(openapi, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
