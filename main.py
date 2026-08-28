from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import init_db
from repository import SQLiteTaskRepository

app = FastAPI()
repo = SQLiteTaskRepository()

init_db()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool = False


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return repo.get_all()


@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    return repo.create(task.title)


@app.put("/tasks/{task_id}", summary="Update a task's title or done status")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    updated = repo.update(task_id, task.title, task.done)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return