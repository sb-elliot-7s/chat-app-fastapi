from sqlalchemy import func, Column, Integer, String, DateTime, Boolean, \
    ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Customers(Base):
    __tablename__ = 'customers'

    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    username = Column(String(length=200))
    password = Column(String)
    bio = Column(String(length=255))
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, server_default=func.now())

    images = relationship(
        'CustomerImage',
        backref='customer',
        passive_deletes=True,
        # lazy='joined'
    )


class CustomerImage(Base):
    __tablename__ = 'customer_images'

    id = Column(Integer, primary_key=True)
    photo = Column(String)

    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
