from const import POSTGRES_PASSWORD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(f"postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/postgres")
engine.connect()
Session = sessionmaker(bind=engine)
