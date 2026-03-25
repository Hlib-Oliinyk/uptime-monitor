from fastapi import APIRouter

from .routes.auth import router as auth_router
from .routes.monitor import router as monitor_router
from .routes.check import router as check_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(monitor_router)
router.include_router(check_router)