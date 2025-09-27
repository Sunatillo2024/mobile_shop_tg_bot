from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=func.now())

    cart_items = relationship("CartItem", back_populates="user")
    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")


class CartItem(Base):
    __tablename__ = "cartitems" # noqa
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items", overlaps="cart_items")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String)
    available = Column(Integer)

    category = relationship("Category", back_populates="products", overlaps="products")
    cart_items = relationship("CartItem", back_populates="product", overlaps="product")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    address_text = Column(String)

    user = relationship("User", back_populates="addresses")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship("Product", back_populates="category", overlaps="category")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    total_price = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "orderitems" # noqa
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_order = Column(Float)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")  # Optional: add back_populates if needed


