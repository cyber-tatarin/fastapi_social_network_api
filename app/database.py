from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}' \
                          f':{settings.database_password}@{settings.database_hostname}' \
                          f':{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#while True:

#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='13012004',
#                                cursor_factory=RealDictCursor)

#        cursor = conn.cursor()
#
#        print('Database is swagging')
#        break

#    except Exception as error:

#       print("Database is under the weather")
#        print("Error: ", error)

#       time.sleep(2)