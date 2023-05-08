from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base
from src.database.db import engine
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birthday = Column(String)
    additional_data = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)
