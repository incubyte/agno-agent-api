from sqlmodel import Session, create_engine
from app.core.setting import settings


engine = create_engine(
    settings.DATABASE_URL, connect_args={}
)

session  = Session(bind=engine)
