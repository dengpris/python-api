from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[int] = mapped_column()
    
    __table_args__ = (
        CheckConstraint('priority BETWEEN 1 AND 5', name='check_priority_range'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class User(UserMixin, db.Model):
    username = db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))

    def get_id(self):
        return (self.username)
   
    def get(user_id):
        return User.query.filter_by(username='user_id').first()