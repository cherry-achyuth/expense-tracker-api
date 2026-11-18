from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,Session
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise RuntimeError("database_url is not configured")

engine = create_engine(database_url,pool_pre_ping = True)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    expire_on_commit = False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    database_test_url = os.getenv('TEST_DATABASE_URL')

    if not database_test_url:
        raise RuntimeError("test_database_url not found")

    test_engine = create_engine(database_test_url,pool_pre_ping=True)

    TestSessionLoader = sessionmaker(
        bind = test_engine,
        autoflush=False,
        expire_on_commit=False
    )

    db = TestSessionLoader()

    try:
        yield db
    finally:
        db.close()
        test_engine.dispose()