"""FastAPI application and API routes."""
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse, TodoUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB. Shutdown: nothing."""
    init_db()
    yield


app = FastAPI(
    title="Todo API",
    description="CRUD API for todo items",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files and serve UI
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """Serve the todo UI."""
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Todo API", "docs": "/docs"}


@app.get("/api/health")
def health():
    """Health check for Docker/CI."""
    return {"status": "ok", "timestamp": time.time()}


@app.get("/api/todos", response_model=list[TodoResponse])
def list_todos(
    completed: bool | None = None,
    db: Session = Depends(get_db),
):
    """List all todos, optionally filtered by completed."""
    q = db.query(Todo)
    if completed is not None:
        q = q.filter(Todo.completed == completed)
    return q.order_by(Todo.created_at.desc()).all()


@app.post("/api/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo."""
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a single todo by ID."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo (partial update)."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(todo, k, v)
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return None
