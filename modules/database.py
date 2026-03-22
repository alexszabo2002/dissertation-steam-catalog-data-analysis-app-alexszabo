from sqlalchemy import create_engine, Column, Boolean, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class GameQueue(Base):
    __tablename__ = 'games_queue'
    appid = Column(Integer, primary_key=True)
    name = Column(String)
    owners = Column(String)
    status = Column(String, default='pending') # 'pending', 'processed', 'error'

class GameDetails(Base):
    __tablename__ = 'game_details'
    
    appid = Column(Integer, primary_key=True)
    name = Column(String)
    is_free = Column(Boolean)
    detailed_description = Column(Text) # Text is better for long strings
    short_description = Column(Text)
    header_image = Column(String)
    website = Column(String)
    developers = Column(String)
    publishers = Column(String)
    initial_price = Column(String) # Storing as formatted string: "19.99 USD"
    final_price = Column(String) # Storing as formatted string: "19.99 USD"
    categories = Column(String) # Store as comma-separated
    genres = Column(String) # Store as comma-separated
    screenshot1 = Column(String)
    screenshot2 = Column(String)
    screenshot3 = Column(String)
    recommendations = Column(Integer)
    release_date = Column(String)
    background_image = Column(String)

# Initialization of the DB file in the /data folder
engine = create_engine('sqlite:///data/steam_catalog.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
