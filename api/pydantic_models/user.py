from pydantic import BaseModel, ConfigDict


class LoginIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    password: str


class LoginOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str


class RegisterIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str | None = None
    login: str
    password: str


class RegisterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str


class ChangeUserIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
