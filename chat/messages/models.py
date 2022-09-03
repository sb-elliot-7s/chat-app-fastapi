from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func, \
    Boolean
from sqlalchemy.orm import relationship
from database import Base


class Message(Base):
    __tablename__ = 'messages'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    text = Column(String)
    from_customer_id = Column(
        Integer,
        ForeignKey('customers.id', ondelete='CASCADE')
    )
    to_customer_id = Column(
        Integer,
        ForeignKey('customers.id', ondelete='CASCADE'),
        nullable=True
    )
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    read = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    channel_id = Column(Integer, ForeignKey('channels.id', ondelete='CASCADE'))

    images = relationship(
        'Image', backref='message', passive_deletes=True, lazy='joined')

    def __repr__(self) -> str:
        return f'Message: {self.text[:20]}'


class Image(Base):
    __tablename__ = 'images'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    message_id = Column(Integer, ForeignKey('messages.id', ondelete='CASCADE'))
    created = Column(DateTime, default=func.now())

    def __repr__(self) -> str:
        return f'Image: {self.photo_url}'
