import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class Deliveryman(Base):
    __tablename__ = 'deliverymen'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    reg_date = Column(DateTime, default=datetime.datetime.now)
    phone = Column(String)
    city = Column(String)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
