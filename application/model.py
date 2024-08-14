from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class TodoItem(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[int] = mapped_column()
    
    __table_args__ = (
        CheckConstraint('priority BETWEEN 1 AND 5', name='check_priority_range'),
    )