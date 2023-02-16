from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from dotenv import load_dotenv
import os

load_dotenv()

if not database_exists(os.getenv("DATABASE_URL")):
    create_database(os.getenv("DATABASE_URL"))

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()