from app.core.database import Base
from sqlalchemy import Integer, String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    userid: Mapped[int] = mapped_column(Integer, nullable= False, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text('TRUE'))
    fullname: Mapped[str] = mapped_column(String(50), nullable=True, server_default=text('TRUE'))
    email: Mapped[EmailStr] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
