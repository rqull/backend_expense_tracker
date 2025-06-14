# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure the database engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # number of connections to keep open
    max_overflow=10,  # max number of connections to create beyond pool_size
    pool_timeout=30,  # timeout for getting a connection from pool
    pool_recycle=1800,  # recycle connections after 30 minutes
    echo=False  # set to True to log all SQL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
