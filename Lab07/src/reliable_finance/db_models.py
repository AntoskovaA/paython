from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    op_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    operations: Mapped[list["FinancialOperation"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class FinancialOperation(Base):
    __tablename__ = "financial_operations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    date: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    op_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        back_populates="operations",
    )