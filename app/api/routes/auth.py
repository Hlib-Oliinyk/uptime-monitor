from fastapi import APIRouter, Depends

from app.services.user import UserService
from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user = await service.create_user(data)
    return user