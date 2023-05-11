from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

MYSQL_HOST = config['mysql']['host']
MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['password']
MYSQL_DB = config['mysql']['db']
MYSQL_PORT = int(config['mysql'].get('port', '3306'))
MYSQL_CHARSET = config['mysql'].get('charset', 'utf8mb4')

engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}", pool_pre_ping=True, pool_recycle=3600, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def execute(sql):
    with engine.connect() as conn:
        result = conn.execute(sql)
    return result

def fetch_one(sql):
    with engine.connect() as conn:
        result = conn.execute(sql).fetchone()
    return result

def fetch_all(sql):
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return result

def add(obj):
    session = Session()
    session.add(obj)
    session.commit()

def delete(obj):
    session = Session()
    session.delete(obj)
    session.commit()

def update():
    session = Session()
    session.commit()
