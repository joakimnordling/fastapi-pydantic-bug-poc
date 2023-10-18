import json
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple, Union

from fastapi import routing
from fastapi._compat import GenerateJsonSchema, ModelField, get_compat_model_name_map
from fastapi.dependencies.utils import get_flat_params
from fastapi.openapi.constants import REF_TEMPLATE
from fastapi.types import ModelNameMap
from pydantic.json_schema import JsonSchemaValue
from starlette.routing import BaseRoute


def patched_get_definitions(
    *,
    fields: List[ModelField],
    schema_generator: GenerateJsonSchema,
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
    Dict[str, Dict[str, Any]],
]:
    override_mode: Union[Literal["validation"], None] = (
        None if separate_input_output_schemas else "validation"
    )
    inputs = [
        (field, override_mode or field.mode, field._type_adapter.core_schema)
        for field in fields
    ]
    field_mapping, definitions = schema_generator.generate_definitions(inputs=inputs)

    print("---")
    print(json.dumps(definitions, indent=2))
    print("---")

    return field_mapping, definitions  # type: ignore[return-value]


def get_fields_from_routes(
    routes: Sequence[BaseRoute],
) -> List[ModelField]:
    body_fields_from_routes: List[ModelField] = []
    responses_from_routes: List[ModelField] = []
    request_fields_from_routes: List[ModelField] = []
    callback_flat_models: List[ModelField] = []
    for route in routes:
        if getattr(route, "include_in_schema", None) and isinstance(
            route, routing.APIRoute
        ):
            if route.body_field:
                assert isinstance(
                    route.body_field, ModelField
                ), "A request body must be a Pydantic Field"
                body_fields_from_routes.append(route.body_field)
            if route.response_field:
                responses_from_routes.append(route.response_field)
            if route.response_fields:
                responses_from_routes.extend(route.response_fields.values())
            if route.callbacks:
                callback_flat_models.extend(get_fields_from_routes(route.callbacks))
            params = get_flat_params(route.dependant)
            request_fields_from_routes.extend(params)

    flat_models = callback_flat_models + list(
        body_fields_from_routes + responses_from_routes + request_fields_from_routes
    )
    return flat_models


def get_fake_openapi(
    *,
    title: str,
    version: str,
    openapi_version: str = "3.1.0",
    summary: Optional[str] = None,
    description: Optional[str] = None,
    routes: Sequence[BaseRoute],
    webhooks: Optional[Sequence[BaseRoute]] = None,
    tags: Optional[List[Dict[str, Any]]] = None,
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    terms_of_service: Optional[str] = None,
    contact: Optional[Dict[str, Union[str, Any]]] = None,
    license_info: Optional[Dict[str, Union[str, Any]]] = None,
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    info: Dict[str, Any] = {"title": title, "version": version}
    if summary:
        info["summary"] = summary
    if description:
        info["description"] = description
    if terms_of_service:
        info["termsOfService"] = terms_of_service
    if contact:
        info["contact"] = contact
    if license_info:
        info["license"] = license_info
    output: Dict[str, Any] = {"openapi": openapi_version, "info": info}
    if servers:
        output["servers"] = servers
    all_fields = get_fields_from_routes(list(routes or []) + list(webhooks or []))
    print("---all_fields---")
    print(all_fields)
    print("---/all_fields---")
    model_name_map = get_compat_model_name_map(all_fields)
    schema_generator = GenerateJsonSchema(ref_template=REF_TEMPLATE)
    patched_get_definitions(
        fields=all_fields,
        schema_generator=schema_generator,
        model_name_map=model_name_map,
        separate_input_output_schemas=separate_input_output_schemas,
    )
