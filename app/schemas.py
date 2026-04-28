from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Fields that are shared by task request and response models."""

    # A task needs a real title. Field(...) lets Pydantic validate the value
    # before the route function runs.
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False

    # Reject unexpected JSON fields so clients notice typos early.
    model_config = ConfigDict(extra="forbid")


class TaskCreate(TaskBase):
    """Data the client sends when creating a new task."""

    pass


class TaskUpdate(TaskBase):
    """Data the client sends when replacing an existing task."""

    pass


class Task(TaskBase):
    """Data the API sends back to the client."""

    id: int
