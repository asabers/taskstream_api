from sqlalchemy.orm import Session
from src import models, schemas

class TaskService:
    def get_tasks(self, db: Session, skip: int = 0, limit: int = 100):
        
        return db.query(models.Task).offset(skip).limit(limit).all()

    def create_user_task(self, db: Session, task: schemas.TaskCreate, user_id: int):
        # Follow the same pattern as other endpoints
        
        db_task = models.Task(**task.dict(), owner_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update_task_status(self, db: Session, task_id: int):
        
        #Update the status
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            db_task.status = "COMPLETED"
            db.commit()
        return db_task

    def trigger_notifications(self, task_id: int):
        
        # TODO: Implement notification logic here.

        pass