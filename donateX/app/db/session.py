from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import MYSQL_CONNECTION


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://{}".format(MYSQL_CONNECTION)


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, pool_pre_ping=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
