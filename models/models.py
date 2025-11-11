# models/models.py
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=True)
    password_hash = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(50))
    region = Column(String(120))  # المحافظة / المنطقة
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    external_id = Column(String(120), index=True, nullable=True)
    customer_name = Column(String(200))
    phone = Column(String(50))
    address = Column(Text)
    region = Column(String(120))  # المحافظة
    items = Column(Text)  # JSON string or CSV
    status = Column(String(50), default='new')  # new, assigned, in_progress, delivered, closed
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)
    agent = relationship('Agent')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    shopify_id = Column(String(120), unique=True, index=True)
    title = Column(String(300))
    description = Column(Text)
    price = Column(Float)
    metadata = Column(Text)  # JSON string
    last_synced = Column(DateTime)

class KBArticle(Base):
    __tablename__ = 'kb_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(300))
    content = Column(Text)
    source = Column(String(200))
    tags = Column(String(300))
    created_at = Column(DateTime, default=datetime.utcnow)

class PostRule(Base):
    """Rule to auto-comment or send a message for a specific post/page"""
    __tablename__ = 'post_rules'
    id = Column(Integer, primary_key=True)
    page_id = Column(String(80))         # facebook page id
    post_id = Column(String(120), index=True, nullable=True) # specific post (null for any post on page)
    rule_name = Column(String(200))
    action_type = Column(String(50))     # "comment", "reply_private", "assign_agent"
    payload = Column(Text)               # JSON with message template, variables, agent assignment rules
    active = Column(Boolean, default=True)

class MessageLog(Base):
    __tablename__ = 'message_logs'
    id = Column(Integer, primary_key=True)
    platform = Column(String(50))   # facebook/whatsapp/internal
    direction = Column(String(10))  # inbound/outbound
    user_id = Column(Integer, nullable=True)
    agent_id = Column(Integer, nullable=True)
    content = Column(Text)
    meta = Column(Text)             # JSON: message ids, post id, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
