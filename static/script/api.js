const baseUrl = "http://localhost:8000";

async function getRootTasks(){
    const url = `${baseUrl}/tasks/roots`;
    let response = await fetch(url);
    return await response.json();
}

async function createTask({name, description=null, parent=null, creator=null}){
    parameters = `name=${name}`
    if(description != null) parameters += `&description=${encodeURIComponent(description)}`;
    if(parent != null) parameters += `&parent=${encodeURIComponent(parent)}`;
    if(creator != null) parameters += `&creator=${encodeURIComponent(creator)}`;
    const url = `${baseUrl}/tasks/create?${parameters}`;
    let response = await fetch(url);
    return await response.json();
}

async function getTask(id){
    const url = `${baseUrl}/tasks/${id}`;
    const response = await fetch(url);
    return await response.json();
}

async function getChildrenTasks(id){
    const url = `${baseUrl}/tasks/${id}/tasks`;
    const response = await fetch(url);
    return await response.json();
}

async function getUsers(){
    const url = `${baseUrl}/users`;
    const response = await fetch(url);
    return await response.json();
}

async function getUsersOfTask(id){
    const url = `${baseUrl}/tasks/${id}/users`;
    const response = await fetch(url);
    return await response.json();
}

async function setName(id, name){
    const url = `${baseUrl}/tasks/${id}/set-name?value=${encodeURIComponent(name)}`;
    const response = await fetch(url);
    return await response.json();
}

async function setDescription(id, description){
    const url = `${baseUrl}/tasks/${id}/set-description?value=${encodeURIComponent(description)}`;
    const response = await fetch(url);
    return await response.json();
}

async function setUser(id, user){
    const url = user? 
        `${baseUrl}/tasks/${id}/set-user?value=${encodeURIComponent(user)}`:
        `${baseUrl}/tasks/${id}/set-user`;
    const response = await fetch(url);
    return await response.json();
}

async function setDueDate(id, dueDate){
    const url = `${baseUrl}/tasks/${id}/set-due-date-epoch?value=${encodeURIComponent(dueDate)}`;
    const response = await fetch(url);
    return await response.json();
}

async function complete(id){
    const url = `${baseUrl}/tasks/${id}/complete`;
    const response = await fetch(url);
    return await response.json();
}

async function getParents(id){
    const url = `${baseUrl}/tasks/${id}/parents`;
    const response = await fetch(url);
    return await response.json();
}