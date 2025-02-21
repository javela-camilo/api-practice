from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import models
from database import engine, SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI(
    title="API Tasks",
    description="API para gestionar tareas",
    version="1.0.0"
)

# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear una instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tasks = [
    {"id": 1, "title": "Aprender HTTP", "done": False},
    {"id": 2, "title": "Hacer API REST", "done": False},
]

# Task model
class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskUpdate(BaseModel):
    title: str
    done: bool

# Raiz
@app.get("/")
def read_root():
    return {"message": "Hello TaskApi"}

# Obtener todas las tasks (sin conexion a la base de datos)
#@app.get("/tasks", summary="Obtener todas las tasks", description="Obtiene todas las tasks disponibles")
#def get_tasks():
#    return tasks

# Obtener todas las tasks
@app.get("/tasks", summary="Obtener todas las tasks", description="Obtiene todas las tasks disponibles")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


# Crear una nueva task (sin conexion a la base de datos)
#@app.post("/tasks", summary="Crear una nueva task", description="Crea una nueva task")
#def create_task(task: Task):
#    tasks.append(task)
#    return JSONResponse(status_code=201, content={"message": "Task created", "task": task.dict()})

# Crear una nueva task
@app.post("/tasks", summary="Crear una nueva task", description="Crea una nueva task")
def create_task_db(task: Task, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title, done=task.done, id_task=task.id)   
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return JSONResponse(status_code=201, content={"message": "Task created", "task": task.dict()})

# Obtener una task por su id (sin conexion a la base de datos)
#@app.get("/tasks/{task_id}", summary="Obtener task por su id", description="Obtiene una task por su id")
#def get_task_by_id(task_id: int):
#    for task in tasks:
#       if task["id"] == task_id:
#            return task
#    raise HTTPException(status_code=404, detail="Task not found")


# Obtener una task por su id
@app.get("/tasks/taskbyid/{task_id}", summary="Obtener task por su id", description="Obtiene una task por su id")
def get_task_by_id_db(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    #return {"id": task.id_task, "title": task.title, "done": task.done}
    return JSONResponse(status_code=201, content={"message": "Task obtained", "id": task.id_task, "title": task.title, "done": task.done})


# Eliminar una task por su id (sin conexion a la base de datos)
#@app.delete("/tasks/delete/{task_id}", summary="Eliminar task por su id", description="Elimina una task por su id")
#def delete_task(task_id: int):
#    for index, task in enumerate(tasks):
#        if task["id"] == task_id:
#            tasks.pop(index)
#            return JSONResponse(status_code=204, content={"message": "Task deleted"})
#    raise HTTPException(status_code=404, detail="Task not found")


# Eliminar una task por su id
@app.delete("/tasks/delete/{task_id}", summary="Eliminar task por su id", description="Elimina una task por su id")
def delete_task_db(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return JSONResponse(status_code=204, content={"message": "Task deleted"})

# Actualizar una task por su id (sin conexion a la base de datos)
#@app.put("/tasks/update/{task_id}", summary="Actualizar task por su id", description="Actualiza una task por su id")
#def update_task(task_id: int, updatedTask: TaskUpdate):
#    for task in tasks:
#        if task["id"] == task_id:
#            task.update(updatedTask.model_dump())
#            return {"message": "Task updated"}
#    raise HTTPException(status_code=404, detail="Task not found")

# Actualizar una task por su id
@app.put("/tasks/update/{task_id}", summary="Actualizar task por su id", description="Actualiza una task por su id")
def update_task_db(task_id: int, updatedTask: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updatedTask.title
    task.done = updatedTask.done
    db.commit()
    db.refresh(task)
    return JSONResponse(status_code=200, content={"message": "Task updated"})
