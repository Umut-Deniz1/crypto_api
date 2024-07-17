import socket
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.conf.settings import Settings

settings = Settings()


def is_reachable(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=5)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        return True
    except OSError:
        return False


if not is_reachable(settings.POSTGRES_HOST, settings.POSTGRES_PORT):
    settings.POSTGRES_HOST = "localhost"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=False,
    echo_pool=False,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
