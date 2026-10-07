import os
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DATA_DIR, "gamezone.db")
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String)
    price = Column(Float, nullable=False)
    age_rating = Column(String)
    image = Column(String)
    description = Column(Text)
    specs = Column(JSON, default=dict)
    in_stock = Column(Integer, default=1)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "age_rating": self.age_rating,
            "image": self.image,
            "description": self.description,
            "specs": self.specs or {},
            "in_stock": bool(self.in_stock),
            "rating": self.rating,
            "review_count": self.review_count,
        }


class Policy(Base):
    __tablename__ = "store_policy"
    id = Column(Integer, primary_key=True, default=1)
    payment = Column(String)
    shipping_cost = Column(Float)
    free_shipping_over = Column(Float)
    delivery_time = Column(String)
    return_policy = Column(Text)
    suspicious_order_threshold = Column(Float)
    max_items_per_order = Column(Integer)
    max_same_item = Column(Integer)

    def to_dict(self):
        return {
            "payment": self.payment,
            "shipping_cost": self.shipping_cost,
            "free_shipping_over": self.free_shipping_over,
            "delivery_time": self.delivery_time,
            "return_policy": self.return_policy,
            "suspicious_order_threshold": self.suspicious_order_threshold,
            "max_items_per_order": self.max_items_per_order,
            "max_same_item": self.max_same_item,
        }


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    customer_address = Column(String)
    items = Column(JSON, default=list)
    item_count = Column(Integer, default=0)
    subtotal = Column(Float, default=0)
    shipping = Column(Float, default=0)
    total = Column(Float, default=0)
    payment = Column(String, default="Cash on delivery")
    timestamp = Column(String)
    status = Column(String, default="pending_ai")
    ai_analysis = Column(JSON, default=None)
    admin_decision = Column(String, default="")
    admin_note = Column(String, default="")

    invoice = relationship("Invoice", back_populates="order", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_address": self.customer_address,
            "items": self.items or [],
            "item_count": self.item_count,
            "subtotal": self.subtotal,
            "shipping": self.shipping,
            "total": self.total,
            "payment": self.payment,
            "timestamp": self.timestamp,
            "status": self.status,
            "ai_analysis": self.ai_analysis,
            "admin_decision": self.admin_decision,
            "admin_note": self.admin_note,
        }


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True)
    product_id = Column(String)
    customer_name = Column(String)
    rating = Column(Integer, default=5)
    text = Column(Text)
    timestamp = Column(String)
    status = Column(String, default="pending_ai")
    ai_analysis = Column(JSON, default=None)
    admin_decision = Column(String, default="")
    admin_note = Column(String, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_name": self.customer_name,
            "rating": self.rating,
            "text": self.text,
            "timestamp": self.timestamp,
            "status": self.status,
            "ai_analysis": self.ai_analysis,
            "admin_decision": self.admin_decision,
            "admin_note": self.admin_note,
        }


class Activity(Base):
    __tablename__ = "activity"
    id = Column(String, primary_key=True)
    timestamp = Column(String)
    action = Column(String)
    actor = Column(String)
    details = Column(Text)
    ref_id = Column(String, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "action": self.action,
            "actor": self.actor,
            "details": self.details,
            "ref_id": self.ref_id,
        }


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    customer_name = Column(String)
    customer_address = Column(String)
    issued_at = Column(String)
    subtotal = Column(Float, default=0)
    shipping = Column(Float, default=0)
    total = Column(Float, default=0)
    status = Column(String, default="unpaid")
    paid_at = Column(String, default="")

    order = relationship("Order", back_populates="invoice")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "issued_at": self.issued_at,
            "subtotal": self.subtotal,
            "shipping": self.shipping,
            "total": self.total,
            "status": self.status,
            "paid_at": self.paid_at,
            "items": self.order.items if self.order else [],
        }


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    Base.metadata.create_all(engine)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
