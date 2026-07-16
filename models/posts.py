from core.database import Base
from sqlalchemy import Integer, String, TIMESTAMP, text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content:  Mapped[str] = mapped_column(String, server_default='TRUE')
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    created_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.userid', ondelete='CASCADE'), nullable=False)
    user = relationship('User')

class Vote(Base):
    __tablename__ = "votes"

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.post_id', ondelete= 'CASCADE'), primary_key= True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.userid', ondelete='CASCADE'), primary_key=True)