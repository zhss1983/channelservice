from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from communication.const import DEBUG, POSTGRES_PASSWORD

if DEBUG:
    engine = create_engine("sqlite:///:memory:", echo=True)
else:
    engine = create_engine(
        f"postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/postgres",
        echo=True,
    )

engine.connect()
Session = sessionmaker(bind=engine)
