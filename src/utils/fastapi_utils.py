"""
====================================================
@Project:   nginx-DL -> fastapi_utils
@Author:    TropicalAlgae
@Date:      2023/6/8 14:01
@Desc:
====================================================
"""

from datetime import datetime
from typing import Union

import pytz
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response


def resp_200(*, data: Union[list, dict, str], message='success') -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 200,
            'message': message,
            'timestamp': str(datetime.now(tz=pytz.timezone('Asia/Shanghai'))),
            'data': data,
        }
    )


def resp_500(*, data: Union[list, dict, str], message: str = "服务器错误") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 500,
            'message': message,
            'timestamp': str(datetime.now(tz=pytz.timezone('Asia/Shanghai'))),
            'data': data,
        }
    )


def add_exception_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def validation_exception_handler(request, exc):
        return resp_500(data=str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return resp_500(data=str(exc))

    @app.exception_handler(Exception)
    async def validation_exception_handler(request, exc):
        return resp_500(data=str(exc))


def custom_openapi_prefix(app: FastAPI, service_name: str):
    def custom_openapi():
        if not app.openapi_schema:
            app.openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                terms_of_service=app.terms_of_service,
                contact=app.contact,
                license_info=app.license_info,
                routes=app.routes,
                tags=app.openapi_tags,
                servers=app.servers,
            )
            temp_path = {}
            for path in app.openapi_schema['paths']:
                val = app.openapi_schema['paths'][path].copy()
                temp_path['/' + service_name + path] = val
            app.openapi_schema['paths'] = temp_path
        return app.openapi_schema

    app.openapi = custom_openapi
