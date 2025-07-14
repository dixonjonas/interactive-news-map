from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String, unique=True)
    summary = Column(Text)
    publish_date = Column(Date)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(String)
    source_url = Column(String)
    raw_json = Column(Text)

# Setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "articles.db")
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
