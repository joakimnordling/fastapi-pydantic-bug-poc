from pydantic import BaseModel, Field


class MyModel(BaseModel):
    my_int: int = Field(
        ...,
    )
