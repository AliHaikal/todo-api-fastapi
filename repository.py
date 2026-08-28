from sqlmodel import Session, select
from models import Task, engine


class SQLiteTaskRepository:
    def get_all(self) -> list[Task]:
        with Session(engine) as session:
            return session.exec(select(Task)).all()

    def get(self, task_id: int) -> Task | None:
        with Session(engine) as session:
            return session.get(Task, task_id)

    def create(self, title: str) -> Task:
        with Session(engine) as session:
            task = Task(title=title, done=False)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                return None
            task.title = title
            task.done = done
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def delete(self, task_id: int) -> bool:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                return False
            session.delete(task)
            session.commit()
            return True