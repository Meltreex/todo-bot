from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional

from app.db.database import Base

class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    
    tasks: Mapped["TaskOrm"] = relationship(back_populates="owner")

class TaskOrm(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    owner: Mapped["UserOrm"] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"TaskOrm(id={self.id}, title={self.title}, description={self.description})"