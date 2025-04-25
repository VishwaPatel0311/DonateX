import typing

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.error_code import err


class APIResponse(BaseModel):
    status: str = "success"
    data: typing.Any = None
    # status_code: int = 200
    # message: str = None


def create_response(data: dict, msg: str = None) -> JSONResponse:

    response = APIResponse(data=data, message=msg)
    return JSONResponse(content=jsonable_encoder(response, by_alias=True))


def create_error_response(error: int = 100, msg: str = None) -> JSONResponse:
    message = err[error]
    if msg:
        for arg in msg:
            message += str(arg)
    data = {"error_code": error, "error_message": message}
    status = "failure"
    resp = APIResponse(status=status, data=data, message=message)
    return JSONResponse(content=jsonable_encoder(resp, by_alias=True))


