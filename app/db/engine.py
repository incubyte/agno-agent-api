from sqlmodel import Session, create_engine
from app.core.setting import settings


engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

session  = Session(bind=engine)
