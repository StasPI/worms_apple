from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class RootZone(Base):
    __tablename__ = 'root_zone'

    id = Column(Integer, primary_key=True)
    name_zone = Column(String(64), nullable=False)


engine = create_engine(
    'postgresql+psycopg2://postgres:testpass@localhost:5432/www', echo=True)

Base.metadata.create_all(engine)
