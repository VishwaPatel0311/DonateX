from fastapi import APIRouter

from .endpoints.auth_apis import auth_router
from .endpoints.donate_apis import donatex_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(donatex_router)

