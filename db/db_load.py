from sqlalchemy.orm import sessionmaker
from db_models import RootZone, Base
from db_connect import db_engine

from pars_data.pars_domains_zone import parser_domains_zone

domains_zone_list = parser_domains_zone()


engine = db_engine()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# one = RootZone(name_zone="Чистый Python") 
# session.add(one) 
# session.commit()


for name in domains_zone_list:
    session.add(RootZone(name_zone=name))

session.commit()

# b = session.query(RootZone).all()
# for i in b:
#     print(i.name_zone)

# print(len(b))

# session.close()