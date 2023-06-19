from app.models.database import Base, SessionLocal, engine
from sqlalchemy.orm import Session


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db() -> None:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
