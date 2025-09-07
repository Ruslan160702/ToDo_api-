from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def creat_task(
    task_in: schemas.TaskCreate,
    db: Session= Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    task = model.task(
        title=task_in.title,
        description=task_in.description
        is_done=task_in.in_done
        ower_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=list[schemas.TaskRead])
def list_my_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User - Depends(get_current_user),
):
    return db.query(models.Task).filter(models.Task.ower_id == current_user,id).all()

@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(
    task_id: int,
    db: Session= Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    task = (
        db.query(models.Task)
        .filter(modle.Task.id == task_id, models.Task.ower_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404. detail="Задача не найдена")
    return task


@router.get("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate, 
    db: Session = Depends(get_db)
    current_user: model.User = Depends(get_current_user),
)
    task = (
        ddb.query(models.Task)
        .filter(modle.Task.id == task_id, models.Task.ower_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404. detail="Задача не найдена")

    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.done is not None:
        task.in_done = task_in.done

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
    current_user: model.User = Depends(get_current_user),
):
    task = (
        ddb.query(models.Task)
        .filter(modle.Task.id == task_id, models.Task.ower_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404. detail="Задача не найдена")

    db.delete(task)
    db.commit()
    return None