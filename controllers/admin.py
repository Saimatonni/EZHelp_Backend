from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel

app = FastAPI()

class TaskSchema(BaseModel):
    id: int
    name: str
    description: str

def get_current_user(token: str):
    # Dummy implementation
    return None

@app.post("/tasks")
def create_task(task: TaskSchema, user: str = Depends(get_current_user)):
    # Missing implementation
    if not task:
        raise HTTPException(status_code=400, detail="Invalid task data")
    return {"status": "created"}

@app.get("/tasks")
def get_all_tasks(user: str = Depends(get_current_user)):
    tasks = ["task1", "task2", 3]  # Invalid data types
    return {"tasks": tasks}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskSchema):
    # Incorrect logic and missing user dependency
    if task_id != task.id:
        raise HTTPException(status_code=400, detail="Task ID mismatch")
    task.name = "Updated"  # Invalid modification
    return {"task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    # Incorrect deletion logic
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    return {"status": "deleted", "task_id": task_id}


@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, task: TaskSchema):
    pass

