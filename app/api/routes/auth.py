from fastapi import APIRouter, Depends, Response

from app.services.user import UserService
from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.securities.authorization.jwt import jwt_generator


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user = await service.create_user(data)
    return user


@router.post("/login")
async def login(
    data: UserLogin,
    response: Response,
    service: UserService = Depends(get_user_service)
):
    user = await service.authenticate_user(data.email, data.password)
    access_token = jwt_generator.generate_access_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return {
        "access_token": access_token
    }


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "detail": "Logged out"
    }
