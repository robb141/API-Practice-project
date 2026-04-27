from pydantic import BaseModel


class TaskBase(BaseModel):
    """Fields that are shared by task request and response models."""

    title: str
    completed: bool = False


class TaskCreate(TaskBase):
    """Data the client sends when creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """Data the client can send when updating an existing task.

    Both fields are optional so a client can update just the title or just
    the completed status.
    """

    title: str | None = None
    completed: bool | None = None


class Task(TaskBase):
    """Data the API sends back to the client."""

    id: int
