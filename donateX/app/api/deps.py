import json
import traceback
from typing import Generator

import multipart.exceptions
from starlette.requests import Request

from db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()
