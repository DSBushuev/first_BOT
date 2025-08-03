"""from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, ForeignKey, String, Float, Text, DateTime # Import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import List
import datetime # Import datetime module for timestamps

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase, AsyncAttrs):
    pass

# Product
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    brand: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    in_stock: Mapped[int] = mapped_column(default=0)

    characteristics: Mapped[List["ProductCharacteristic"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class Characteristic(Base):
    __tablename__ = "characteristics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    values: Mapped[List["ProductCharacteristic"]] = relationship(
        back_populates="characteristic", cascade="all, delete-orphan"
    )


class ProductCharacteristic(Base):
    __tablename__ = "product_characteristics"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    characteristic_id: Mapped[int] = mapped_column(ForeignKey("characteristics.id"))
    value: Mapped[str] = mapped_column(String(100))

    product: Mapped["Product"] = relationship(back_populates="characteristics")
    characteristic: Mapped["Characteristic"] = relationship(back_populates="values")


# User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    cart_items: Mapped[List["CartItem"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="addresses")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event: Mapped[str] = mapped_column(String(100))  # Например: 'login', 'quiz_started'
    timestamp: Mapped[str] = mapped_column(String(100))  # Или использовать DateTime

    user: Mapped["User"] = relationship(back_populates="sessions")

# Cart (renamed from 'Orders' section in original file)
class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(back_populates="cart_items")
    product: Mapped["Product"] = relationship()


# Orders
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_amount: Mapped[float] = mapped_column(default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, paid, shipped, canceled
    created_at: Mapped[str] = mapped_column(String(100))  # можно заменить на DateTime

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column()

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

# Administration Tables
class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="manager") # e.g., 'owner', 'manager', 'editor'

    activity_logs: Mapped[List["ActivityLog"]] = relationship(
        back_populates="admin", cascade="all, delete-orphan"
    )


class ActivityLog(Base):
    __tablename__ = "activity_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"))
    event_type: Mapped[str] = mapped_column(String(100)) # e.g., 'product_added', 'price_updated', 'order_status_changed'
    description: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now) # Using DateTime for consistency and best practice

    admin: Mapped["Admin"] = relationship(back_populates="activity_logs")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)"""