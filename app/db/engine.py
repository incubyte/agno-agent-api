from sqlmodel import Session, create_engine
from app.core.setting import settings


print("Initializing database engine...")
print(f"Using database URL: {settings.DATABASE_URL}")
print("sender Email:", settings.SENDER_EMAIL)
engine = create_engine(
    settings.DATABASE_URL, connect_args={}
)

session  = Session(bind=engine)
