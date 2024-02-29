from sqlalchemy import Column, Integer, String, func, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Contact(Base):

    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=True, index=True)
    phone = Column(String(150), unique=True, nullable=False, index=True)
    born_date = Column(Date, nullable=True, index=True)
    created_at = Column(DateTime, default=func.now())

   



