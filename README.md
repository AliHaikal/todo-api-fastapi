# todo-api-fastapi
# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Data is stored in memory and resets when the server restarts.

## Run it

    pip install fastapi uvicorn
    uvicorn main:app --reload --port 8000

Then visit http://localhost:8000/docs for interactive Swagger docs.

## Endpoints

| Method | Path         | Description         |
|--------|--------------|----------------------|
| GET    | /            | API info             |
| GET    | /health      | Health check         |
| GET    | /tasks       | List all tasks       |
| GET    | /tasks/{id}  | Get a single task    |
| POST   | /tasks       | Create a new task    |
| PUT    | /tasks/{id}  | Update a task        |
| DELETE | /tasks/{id}  | Delete a task         |

## Example: full CRUD cycle

**1. Create a task**

    curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Hope"}'

Response: `201 Created`, `{"id":4,"title":"Hope","done":false}`

**2. Read it back**

    curl.exe -i http://localhost:8000/tasks/4

Response: `200 OK`, `{"id":4,"title":"Hope","done":false}`

**3. Update it**

    curl.exe -i -X PUT http://localhost:8000/tasks/4 -H "Content-Type: application/json" -d '{"title":"Hope","done":true}'

Response: `200 OK`, `{"id":4,"title":"Hope","done":true}`

**4. Delete it**

    curl.exe -i -X DELETE http://localhost:8000/tasks/4

Response: `204 No Content`

**5. Confirm it's gone**

    curl.exe -i http://localhost:8000/tasks/4

Response: `404 Not Found`, `{"detail":"Task 4 not found"}`

## Swagger UI

![Swagger UI]      Screenshot 2026-08-22 080125.png



## Database

**Why SQLite?**
I've used this befre its easy and light . Als its very fast and ssince this it not a very large project its fits it ..

**Where it's stored**
The database lives in `tasks.db`, created automatically in the 
project root the first time you run the app.

**How to run**
pip install fastapi uvicorn sqlmodel
uvicorn main:app --reload

**Database viewer**

![alt text](<Screenshot 2026-08-26 113832-1.png>)

**Example query**

SELECT * FROM tasks WHERE done = 1;
