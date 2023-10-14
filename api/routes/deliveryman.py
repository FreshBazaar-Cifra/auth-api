from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from auth.auth_handler import sign_jwt
from descriptions.user import *
from models import DeliverymanCred, Deliveryman
from models.db_session import get_session
from pydantic_models.deliveryman import DeliverymanRegister
from pydantic_models.user import LoginOut, LoginIn, RegisterOut
from starlette.responses import JSONResponse
from utils.password import hash_password


router = APIRouter()


@router.post("/register", summary="Register", operation_id="register-deliveryman",
             description=register_user_description, response_model=RegisterOut,
             dependencies=[Depends(JWTBearer(admin=True))])
async def register_deliveryman(register: DeliverymanRegister, session: AsyncSession = Depends(get_session)):

    deliveryman = Deliveryman(first_name=register.first_name, last_name=register.last_name, city=register.city,
                              phone=register.phone)
    session.add(deliveryman)
    try:
        deliveryman_cred = DeliverymanCred(deliveryman_id=deliveryman.id, login=register.login, password=hash_password(register.password))
        await deliveryman_cred.save(session)
    except IntegrityError:
        return JSONResponse(status_code=403, content={"description": "User already exists"})
    deliveryman_cred.deliveryman_id = deliveryman.id
    await session.commit()
    return {"token": sign_jwt("deliveryman_id", deliveryman.id, "delivery", 2592000)}


@router.post("/login", summary="Login deliveryman", operation_id="login-deliveryman",
             description=login_user_description, response_model=LoginOut)
async def login_deliveryman(login: LoginIn, session: AsyncSession = Depends(get_session)):
    deliveryman = await DeliverymanCred.get_by_login(login.login, session)
    if deliveryman and deliveryman.password == hash_password(login.password):
        return {"token": sign_jwt("deliveryman_id", deliveryman.id, "delivery",
                                  2592000)}
    return Response(status_code=403)