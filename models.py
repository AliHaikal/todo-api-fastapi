from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/tasks.db")

# Ensure the folder exists before SQLite tries to create the file
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            session.add(Task(title="Buy milk", done=False))
            session.add(Task(title="Walk the dog", done=True))
            session.add(Task(title="Write README", done=False))
            session.commit()