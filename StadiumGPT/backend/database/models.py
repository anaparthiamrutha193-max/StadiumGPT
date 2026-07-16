from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(primary_key=True)
    full_name: Mapped[str]=mapped_column(String(120), nullable=False)
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str]=mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    chats: Mapped[list['Chat']]=relationship(back_populates='user', cascade='all, delete-orphan')
    notifications: Mapped[list['Notification']]=relationship(back_populates='user', cascade='all, delete-orphan')
class Chat(Base):
    __tablename__='chats'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    message: Mapped[str]=mapped_column(Text, nullable=False)
    response: Mapped[str]=mapped_column(Text, nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user: Mapped[User]=relationship(back_populates='chats')
class Notification(Base):
    __tablename__='notifications'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    title: Mapped[str]=mapped_column(String(200), nullable=False)
    description: Mapped[str]=mapped_column(Text, nullable=False)
    notification_type: Mapped[str]=mapped_column(String(50), default='info', nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user: Mapped[User]=relationship(back_populates='notifications')