from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class URL_MODEL(Base):
    __tablename__="URLs" 
    long_url:Mapped[str]
    short_url:Mapped[str]
    clicks:Mapped[int]=0
    id:Mapped[int] = mapped_column(primary_key=True)