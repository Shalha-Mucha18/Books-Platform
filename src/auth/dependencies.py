from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status, Depends
from .utils import decode_access_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService   
from src.db.main import get_session
from src.db.models import User
from typing import List

user_service = UserService()



class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        # auto_error=False lets us control the error response instead of returning
        # FastAPI's default "Not authenticated" message before our checks run.
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)

        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing bearer token in Authorization header",
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization scheme must be Bearer",
            )

        token = credentials.credentials

        token_data = decode_access_token(token)

        if not self.token_validator(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication token",
            )

        if await token_in_blocklist(token_data.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= {
                    "error": "Token has been revoked",
                    "resolutions": "generate a new token by logging in again" 

                }
            )    

        self.verify_token_data(token_data)
        return token_data

    def token_validator(self, token: str):
        return decode_access_token(token) is not None

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in subclasses")




class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data.get("refresh") is True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token not allowed for this endpoint",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token",
            )

async def get_current_user(
    token_details : dict = Depends(AccessTokenBearer()),
    session : AsyncSession = Depends(get_session)):

    user_email = token_details.get("user").get("email")
    user = await user_service.get_user_by_email(user_email,session)

    return user     

class RoleChecker:
    def __init__(self, allowed_rules:List[str]) -> None:
        self.allowed_rules = allowed_rules


    def __call__(self, current_user : User = Depends(get_current_user)):
        if current_user.role  in self.allowed_rules:
            return True

        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You are not allowed to perform this action"
        )    


            
