import secrets

from app.repositories.token import TokenRepository
from app.models.refresh_token import RefreshToken
from app.exceptions.token import InvalidCredentials
from app.securities.hashing import hash_token
from app.securities.authorization.jwt import jwt_generator


class TokenService:
    def __init__(self, repo: TokenRepository):
        self.repo = repo

    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)

    async def save_new_token(self, token: str) -> RefreshToken:
        refresh_token = await self.repo.get_validate_refresh_token(token)
        if refresh_token is None:
            raise InvalidCredentials()
        return refresh_token

    async def rotate_refresh_token(self, token: str) -> [str, str]:
        token_hash = hash_token(token)

        old_token = await self.repo.get_validate_refresh_token(token_hash)
        if old_token is None:
            raise InvalidCredentials()

        new_refresh_token = self.create_refresh_token()
        new_refresh_token_hash = hash_token(new_refresh_token)

        await self.repo.rotate_token_data(
            old_token.id,
            old_token.user_id,
            new_refresh_token_hash
        )

        new_access_token = jwt_generator.generate_access_token(old_token.user_id)
        return new_refresh_token, new_access_token

    async def delete_refresh_token(self, token: str):
        token_hash = hash_token(token)
        await self.repo.delete_token(token_hash)