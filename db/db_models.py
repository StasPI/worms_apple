from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db_connect import db_engine

Base = declarative_base()


class RootZone(Base):
    __tablename__ = 'root_zone'

    id = Column(BigInteger, primary_key=True)
    name_zone = Column(String(64), nullable=False)


engine = db_engine()
Base.metadata.create_all(engine)
