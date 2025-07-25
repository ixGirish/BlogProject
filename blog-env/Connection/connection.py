from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mssql+pyodbc://girish:GNBu4Ya5xV@ix.innovatechs.com/TRAINING?driver=ODBC Driver 17 for SQL Server"


engine = create_engine(DATABASE_URL, 
    pool_size=2,
    max_overflow=0,
    pool_timeout=2,     # Optional: time to wait before erroring
    connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()