from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from typing import List
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Employee(db.Model):
    __tablename__ = "employee_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    quota: Mapped["Quota"] = relationship(back_populates="employee", uselist=False)
    history: Mapped[List["History"]] = relationship(back_populates="employee")

        
class Quota(db.Model):
    __tablename__ = "quota_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    montly_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee_table.id"), unique=True)
    employee: Mapped["Employee"] = relationship(back_populates="quota")

class History(db.Model):
    __tablename__ = "history_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    packages_taken: Mapped[int] = mapped_column(Integer, nullable=False, default=1) #пополнение по одной транзакции поэтому дефолт 1, но мб хуйня
    date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    #date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    #А это бля устаревший вариант который я заметил уже под конец

    #date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now()) 
    #из того что я понял это более правильный вариант который я нашел уже позже, реализация времени на стороне DB в момент Insert, там еще доп библа должна быть но я убрал 
    #и да да я вкурсе что ты знаешь про библу для себя пишу
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee_table.id"))
    employee: Mapped["Employee"] = relationship(back_populates="history")


