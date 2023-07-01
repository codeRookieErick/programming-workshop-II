from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Callable, Any
import uuid
import json
import random
import time


file:str = 'data.json'

def get_data():
    try:
        with open(file, 'r') as fi:
            return json.load(fi)
    except:
        return {
            "colors": ["#FF0000"],
            "users": [],
            "objectives": []
        }
    
def save_data(data):
    with open(file, 'w') as fo:
        json.dump(data, fo, indent='\t')


def get_task_tree(tasks, id):
    filter = [i for i in tasks if i["id"] == id]
    if filter:
        yield filter[0]
        for child in tasks:
            if child["parent"] == id:
                for c in get_task_tree(tasks, child["id"]):
                    yield c

def get_parents_tree(tasks, id):
    filter = [i for i in tasks if i["id"] == id]
    if filter:
        yield filter[0]
        if filter[0]["parent"]:
            for parent in get_parents_tree(tasks, filter[0]["parent"]):
                yield parent

app = FastAPI()
app.mount("/app", StaticFiles(directory='./static'), name="static")
@app.middleware("http")
async def add_cors(request:Request, call_next):
    response:Response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Methods"] = 'GET, POST'
    response.headers["Access-Control-Allow-Headers"] = '*'
    return response

@app.get("/favicon.ico")
def icon():
    return ""

@app.get("/{path}")
def get(path:str):
    return get_data()[path]

@app.get("/users/create")
def create_user(name:str):
    data = get_data()
    user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "color": random.choice(data["colors"]) 
    }
    data["users"].append(user)
    save_data(data)
    return user

def use_tasks(callback:Callable[[list[dict],], Any]) -> Any:
    data = get_data()
    result = callback(data["tasks"])
    save_data(data)
    return result

def use_task(id:str, callback:Callable[[dict,], Any], change:str) -> Any:
    def inner(tasks):
        filter = [i for i in tasks if i["id"] == id]
        if not filter:
            raise HTTPException(404, f"task {id} not found")
        task = filter[0]
        result = callback(task)
        task["history"].append({
            "epoch": int(time.time()),
            "event": "Cambio",
            "description": change
        })
        return result
    return use_tasks(inner)

@app.get(
        "/tasks/create",
        tags=["Tasks"]
        )
def create_task(name:str, description:str|None = None, parent:str|None = None, creator:str|None = None):
    def inner(tasks:dict):
        new_task = {
            "id": str(uuid.uuid4()),
            "name": name,
            "creator": creator,
            "parent": parent,
            "description": description,
            "due_date_epoch": None,
            "user": None,
            "completed": False,
            "complete_date_epoch": None,
            "assigned_date_epoch": None,
            "history":[
                {
                    "epoch": int(time.time()),
                    "event": "Nuevo",
                    "description": f"Tarea creada." 
                }
            ]
        }
        tasks.append(new_task)
        return new_task
    return use_tasks(inner)

@app.get(
        "/tasks/roots",
        tags=["Tasks"]
        )
def get_root_tasks():
    def inner(tasks:dict):
        return [i for i in tasks if i["parent"] == None]
    return use_tasks(inner)

@app.get(
        "/tasks/{id}",
        tags=["Tasks"]
    )
def get_task(id:str):
    def inner(tasks):
        filter = [i for i in tasks if i["id"] == id]
        if not filter:
            raise HTTPException(404, f"task {id} not found")
        return filter[0]
    return use_tasks(inner)

@app.get(
        "/tasks/{id}/set-{property}-epoch",
        tags=["Tasks"]
        )
def set_task_property_epoch(id:str, property:str, value:int, user:str|None = None):
    user = user or "Alguien"
    property = (property + '_epoch').replace('-', '_')
    def inner(task):
        task[property] = value
        return task
    return use_task(id, inner, f"{user} ha cambiado la propiedad '{property}'. Nuevo valor: {value}")

@app.get(
        "/tasks/{id}/set-{property}",
        tags=["Tasks"]
        )
def set_task_property(id:str, property:str, value:str|None = None, user:str|None = None):
    user = user or "Alguien"
    def inner(task):
        task[property] = value
        return task
    return use_task(id, inner, f"{user} ha cambiado la propiedad '{property}'. Nuevo valor: {value}")

@app.get(
        "/tasks/{id}/complete",
        tags=["Tasks"]
        )
def complete(id:str, user:str|None = None):
    user = user or "unknown"
    def inner(task):
        task["completed"] = True
        task["complete_date_epoch"] = int(time.time())
        return task
    return use_task(id, inner, f"Finalizada por {user}")

@app.get(
        "/tasks/{id}/tasks",
        tags=["Tasks"]
        )
def get_sub_tasks(id:str):
    def inner(tasks):
        return [i for i in tasks if i["parent"] == id]
    return use_tasks(inner)

@app.get("/tasks/{id}/users")
def get_users(id:str):
    def inner(tasks):
        users = get_data()["users"]
        tree = get_task_tree(tasks, id)
        result = [i["user"] for i in tree if i["user"]]
        return [i for i in users if i["id"] in result]
    return use_tasks(inner)

@app.get("/tasks/{id}/parents")
def get_parents(id:str):
    def inner(tasks):
        tree = get_parents_tree(tasks, id)
        return tree
    return use_tasks(inner)
