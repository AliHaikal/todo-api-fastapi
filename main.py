from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
app = FastAPI()



class TaskCreate(BaseModel):
    title: str

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False
    
engine = create_engine("sqlite:///tasks.db")

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            session.add(Task(title="Buy milk", done=False))
            session.add(Task(title="Walk the dog", done=True))
            session.add(Task(title="Write README", done=False))
            session.commit()

init_db()

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    with Session(engine) as session:
        new_task = Task(title=task.title, done=False)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

class TaskUpdate(BaseModel):
    title: str
    done: bool = False

@app.put("/tasks/{task_id}", summary="Update a task's title or done status")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    with Session(engine) as session:
        existing = session.get(Task, task_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        existing.title = task.title
        existing.done = task.done
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing 

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    with Session(engine) as session:
        existing = session.get(Task, task_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        session.delete(existing)
        session.commit()
        return