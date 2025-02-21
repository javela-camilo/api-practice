from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI(
    title="API Tasks",
    description="API para gestionar tareas",
    version="1.0.0"
)

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

# Obtener todas las tasks
@app.get("/tasks", summary="Obtener todas las tasks", description="Obtiene todas las tasks disponibles")
def get_tasks():
    return tasks

# Crear una nueva task
@app.post("/tasks", summary="Crear una nueva task", description="Crea una nueva task")
def create_task(task: Task):
    tasks.append(task)
    return JSONResponse(status_code=201, content={"message": "Task created", "task": task.dict()})

# Obtener una task por su id
@app.get("/tasks/{task_id}", summary="Obtener task por su id", description="Obtiene una task por su id")
def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Eliminar una task por su id
@app.delete("/tasks/delete/{task_id}", summary="Eliminar task por su id", description="Elimina una task por su id")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return JSONResponse(status_code=204, content={"message": "Task deleted"})
    raise HTTPException(status_code=404, detail="Task not found")

# Actualizar una task por su id
@app.put("/tasks/update/{task_id}", summary="Actualizar task por su id", description="Actualiza una task por su id")
def update_task(task_id: int, updatedTask: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(updatedTask.model_dump())
            return {"message": "Task updated"}
    raise HTTPException(status_code=404, detail="Task not found")

