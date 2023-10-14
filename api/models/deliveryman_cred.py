from sqlalchemy import Column, Integer, String, select, update, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class DeliverymanCred(Base):
    __tablename__ = 'deliveryman_creds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deliveryman_id = Column(Integer, ForeignKey("deliverymen.id"))
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @classmethod
    async def get_by_login(cls, login: str, session: AsyncSession):
        """
        Get deliveryman by his id

        :param login: login of deliveryman
        :param session: session
        :return: DeliverymanCred
        :rtype: DeliverymanCred
        """

        _ = await session.execute(select(cls).where(cls.login == login))
        return _.scalar()

    @classmethod
    async def get_by_deliveryman_id(cls, deliveryman_id: int, session: AsyncSession):
        """
        Get deliveryman creds by deliveryman id

        :param deliveryman_id: id of user from db
        :param session: session
        :return: DeliverymanCred
        :rtype: DeliverymanCred
        """

        _ = await session.execute(select(cls).where(cls.deliveryman_id == deliveryman_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
