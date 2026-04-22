from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import models, schemas, database
from src.auth import security
from src.services.task_service import TaskService

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="TaskStream API")
service = TaskService()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # TRAP: Missing actual Auth dependency, hardcoding user_id=1
    return service.create_user_task(db=db, task=task, user_id=1)

@app.get("/tasks/")
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_tasks(db, skip=skip, limit=limit)

@app.put("/tasks/{task_id}/status")
def update_status(task_id: int, db: Session = Depends(get_db)):
    return service.update_task_status(db, task_id)

@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.2-legacy"}