# Proof of Concept for an issue in Pydantic

When generating the json schema of the model(s), the name of the model is not used in
the schema, instead the drive letter is used on Windows machines.

## Running

```shell
poetry install
poetry run run-poc
```

## Details of the issue

If you run this on a Mac you'll get the expected output like this, where the model name
i.e. `MyModel` is used.

```json
{
  "$defs": {
    "MyModel": {
      "properties": {
        "my_int": {
          "title": "My Int",
          "type": "integer"
        }
      },
      "required": ["my_int"],
      "title": "MyModel",
      "type": "object"
    }
  },
  "title": "My Schema"
}
```

And if you run it on Windows you will instead get output where `MyModel` is replaced by
the drive letter, like `C` or `D`, ... (corresponding to `C:` or `D:`, ...) like this:

```json
{
  "$defs": {
    "D": {
      "properties": {
        "my_int": {
          "title": "My Int",
          "type": "integer"
        }
      },
      "required": ["my_int"],
      "title": "MyModel",
      "type": "object"
    }
  },
  "title": "My Schema"
}
```

## Cause

The model is imported using importlib in a fairly untypical way. See the
`import_my_model` function in [pydantic_poc/main.py](pydantic_poc/main.py) for more
details on how it is imported. If you use a relative import instead, the file is not
loaded from `C:` or `D:` and there's no issue. Same applies if you use the normal python
import syntax (`import ... from ...` or import `import ...`).

The function `get_defs_ref` in
[pydantic/json_schema.py](https://github.com/pydantic/pydantic/blob/v2.4.2/pydantic/json_schema.py#L1847)
tries to remove an ID by splitting at a colon `:` character and thus ends up removing
everything after the drive letter, so `C:\Users\...` becomes just `C`.
