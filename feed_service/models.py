from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)  
    feed_items = relationship("FeedItem", back_populates="feed")

class FeedItem(Base):
    __tablename__ = 'feed_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    link = Column(String(255), nullable=False)
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    feed = relationship("Feed", back_populates="feed_items")

class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  
    feed_item_id = Column(Integer, ForeignKey('feed_items.id'))
    feed_item = relationship("FeedItem")