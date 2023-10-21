from sqlalchemy import BigInteger, VARCHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(100), nullable=False)
    enabled: Mapped[bool] = mapped_column("enabled", Boolean, nullable=False, default=False)
