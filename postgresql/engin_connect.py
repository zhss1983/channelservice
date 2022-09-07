from sqlalchemy import Boolean, Column, Float, Integer, MetaData, String, Table, create_engine

DEBUG = True
PASSWORD = "lehrjgjg"

if DEBUG:
    engine = create_engine("sqlite:///:memory:", echo=True)
else:
    # dialect+driver://username:password@host:port/database
    # engine = create_engine(
    #     "postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts",
    #     echo=True, pool_size=6, max_overflow=10, encoding='latin1'
    # )
    # Аргумент	Описание
    # echo	Булево значение. Если задать True, то движок будет сохранять логи SQL в стандартный вывод. По умолчанию значение равно False
    # pool_size	Определяет количество соединений для пула. По умолчанию — 5
    # max_overflow	Определяет количество соединений вне значения pool_size. По умолчанию — 10
    # encoding	Определяет кодировку SQLAlchemy. По умолчанию — UTF-8. Однако этот параметр не влияет на кодировку всей базы данных
    # isolation_level	Уровень изоляции. Эта настройка контролирует степень изоляции одной транзакции. Разные базы данных поддерживают разные уровни. Для этого лучше ознакомиться с документацией конкретной базы данных
    engine = create_engine(f"postgresql+psycopg2://postgres:{PASSWORD}@localhost:5432/postgres", echo=True)

engine.connect()
print(engine)
