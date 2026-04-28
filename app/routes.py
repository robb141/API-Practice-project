from fastapi import APIRouter, HTTPException, status

from app.schemas import Task, TaskCreate, TaskUpdate


router = APIRouter()

# This dictionary is our in-memory "database".
# Data stored here disappears when the server restarts.
tasks: dict[int, Task] = {}

# A simple counter that gives each new task a unique ID.
next_task_id = 1


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple response so clients can check that the API is running."""

    return {"status": "ok"}


@router.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    """Return all tasks currently stored in memory."""

    return list(tasks.values())


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate) -> Task:
    """Create a new task and store it in memory."""

    global next_task_id

    task = Task(id=next_task_id, **task_data.model_dump())
    tasks[task.id] = task
    next_task_id += 1

    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate) -> Task:
    """Replace an existing task by ID."""

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # PUT usually means "replace the whole resource".
    # The ID stays the same because it comes from the URL path.
    updated_task = Task(id=task_id, **task_data.model_dump())
    tasks[task_id] = updated_task

    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    """Delete an existing task by ID."""

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    del tasks[task_id]
