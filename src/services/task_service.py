from sqlalchemy.orm import Session
from src import models, schemas

class TaskService:
    def get_tasks(self, db: Session, skip: int = 0, limit: int = 100):
        # PERFORMANCE  N+1 query 
        return db.query(models.Task).offset(skip).limit(limit).all()

    def create_user_task(self, db: Session, task: schemas.TaskCreate, user_id: int):
        # AMBG: "Follow the same pattern as other endpoints"
        # But there are NO other validation patterns in this file!
        db_task = models.Task(**task.dict(), owner_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update_task_status(self, db: Session, task_id: int):
        """
        INTERPRETATION TRAP: 'Update the status'. 
        To what? It defaults to COMPLETED, but doesn't handle IN_PROGRESS.
        """
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            db_task.status = "COMPLETED"
            db.commit()
        return db_task

    def trigger_notifications(self, task_id: int):
        """
        UNDERSPECIFIED TRAP: Reference to a notification system that isn't built.
        """
        # TODO: Implement notification logic here.
        # Should call the notification service.
        pass