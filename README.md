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

## Containerization (BE-04)

I used Sqllite instead of Postgres 
Reason : there was something wrong with my machine or the system cause the Docker Desktop app was not runnin . neither the uuntu was installing , aslso in A2 i used Sql lite and i was famileire with it so yeah i used sqllite instead of Postgres with the same goals: 
volume-backed persistence, .env-driven config, and one-command 
startup
so, i shifted to github codebase instead 

## Repository pattern
Routes in `main.py` never touch the database directly — they only 
call methods on `SQLiteTaskRepository` (`get_all`, `get`, `create`, 
`update`, `delete`), defined in `repository.py`. The database engine 
and table definition live in `models.py`. This means swapping storage 
implementations only requires changing `repository.py`/`models.py` — 
`main.py` and the API behavior stay identical, which was true both 
before and after containerizing.    

### How persistence was verified
1. Started the stack with `docker compose up --build`
2. Created a new task via `POST /tasks`
3. Ran `docker compose down` to fully stop and remove the container
4. Ran `docker compose up --build` again
5. Called `GET /tasks` and confirmed the task created in step 2 was 
   still present

This confirms data survives not just an app restart, but a full 
container teardown and rebuild — because `tasks.db` lives in a 
Docker volume (`./data:/app/data`) mounted from the host, not inside 
the container's own filesystem.-


### How to run

docker compose up --build

The app will be available on port 8000. `.env.example`