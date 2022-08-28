from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func, Boolean, \
    Table
from sqlalchemy.orm import relationship
from database import Base


# channel_customers = Table(
#     'channels_customers',
#     Base.metadata,
#     Column('customer_id', Integer, ForeignKey('customers.id')),
#     Column('channel_id', Integer, ForeignKey('channels.id')),
#     Column('created', DateTime, default=func.now())
# )


class ChannelsCustomers(Base):
    __tablename__ = 'channels_customers'
    __mapper_args__ = {'eager_defaults': True}

    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    channel_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    created = Column(DateTime, default=func.now())


class Channel(Base):
    __tablename__ = 'channels'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    channel_name = Column(String(length=200), nullable=False)
    describe_info = Column(String(length=255), nullable=True)
    owner_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
    created = Column(DateTime, server_default=func.now())
    online_customers = relationship(
        'Customers', backref='channels', secondary='channels_customers'
    )
    messages = relationship('Message', backref='channel', passive_deletes=True)


class Message(Base):
    __tablename__ = 'messages'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    text = Column(String)
    from_customer_id = Column(Integer,
                              ForeignKey('customers.id', ondelete='CASCADE'))
    to_customer_id = Column(
        Integer,
        ForeignKey('customers.id', ondelete='CASCADE'),
        nullable=True
    )
    created = Column(DateTime, server_default=func.now())
    read = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    channel_id = Column(Integer, ForeignKey('channels.id', ondelete='CASCADE'))

    images = relationship(
        'Image', backref='message', passive_deletes=True, lazy='joined'
    )


class Image(Base):
    __tablename__ = 'images'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    message_id = Column(Integer, ForeignKey('messages.id', ondelete='CASCADE'))
    created = Column(DateTime, default=func.now())
