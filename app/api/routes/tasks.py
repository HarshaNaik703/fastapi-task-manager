from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskRead
from app.db.models import Task, User
from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        priority=task_in.priority,
        status="pending",
        owner_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get(
    "",
    response_model=list[TaskRead]
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).all()

    return tasks


@router.put(
    "/{task_id}",
    response_model=TaskRead
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this task"
        )

    update_data = task_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this task"
        )

    db.delete(task)
    db.commit()

    return None
