from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db() -> None:
    db: Session = SessionLocal()
    with db:
        yield db
