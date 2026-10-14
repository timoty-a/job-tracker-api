from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20))