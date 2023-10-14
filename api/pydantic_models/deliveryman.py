from pydantic import BaseModel, ConfigDict


class DeliverymanRegister(BaseModel):
    first_name: str
    last_name: str | None = None
    login: str
    password: str
    phone: str
    city: str
