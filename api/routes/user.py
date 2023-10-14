from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_handler import sign_jwt
from descriptions.user import *
from models import User, UserCred
from models.db_session import get_session
from pydantic_models.user import LoginOut, LoginIn, RegisterIn, RegisterOut
from starlette.responses import JSONResponse
from utils.password import hash_password


router = APIRouter()


@router.post("/register", summary="Register", operation_id="register",
             description=register_user_description, response_model=RegisterOut)
async def register_user(register: RegisterIn, session: AsyncSession = Depends(get_session)):
    user = User(first_name=register.first_name, last_name=register.last_name)
    session.add(user)
    try:
        user_cred = UserCred(login=register.login, password=hash_password(register.password))
        await user_cred.save(session)
    except IntegrityError:
        return JSONResponse(status_code=403, content={"description": "User already exists"})
    user_cred.user_id = user.id
    await session.commit()
    return {"token": sign_jwt("user_id", user.id, "user", 2592000)}


@router.post("/login", summary="Login", operation_id="login",
             description=login_user_description, response_model=LoginOut)
async def login_user(login: LoginIn, session: AsyncSession = Depends(get_session)):
    user_cred = await UserCred.get_by_login(login.login, session)
    if user_cred and user_cred.password == hash_password(login.password):
        return {"token": sign_jwt("user_id", user_cred.user_id, "user", 2592000)}
    return Response(status_code=403)
