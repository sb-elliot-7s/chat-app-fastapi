from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from ..messages.models import Message


class Subscribers(Base):
    __tablename__ = 'subscribers'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    channel_id = Column(
        Integer,
        ForeignKey('channels.id', ondelete='CASCADE')
    )
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f'Subscriber: {self.customer_id} {self.channel_id}'


class ChannelsCustomers(Base):
    __tablename__ = 'channels_customers'
    __mapper_args__ = {'eager_defaults': True}

    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    channel_id = Column(
        Integer,
        ForeignKey('channels.id', ondelete='CASCADE'), primary_key=True
    )
    created = Column(DateTime, default=func.now())

    def __repr__(self) -> str:
        return f'ChannelsCustomers: {self.customer_id} {self.channel_id}'


class Channel(Base):
    __tablename__ = 'channels'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    channel_name = Column(String(length=200), nullable=False)
    slug = Column(String)
    describe_info = Column(String(length=255), nullable=True)
    owner_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
    created = Column(DateTime, server_default=func.now())
    subscribers = relationship(
        'Customers', backref='channels_subscribe', secondary='subscribers'
    )
    online_customers = relationship(
        'Customers', backref='channels', secondary='channels_customers'
    )
    messages = relationship('Message', backref='channel', passive_deletes=True)

    def __repr__(self) -> str:
        return f'Channel: {self.slug}'
