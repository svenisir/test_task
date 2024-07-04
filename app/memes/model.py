from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Memes(Base):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(TEXT)
    file_name: Mapped[str]

    def __str__(self):
        return f"Mem #{self.id}"
