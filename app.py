from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

import json


app = FastAPI()

class Post(BaseModel):
    id: Optional[str]
    dui: str
    nombre: str
    departamento: str
    municipio: str
    centro_de_votacion: str
    direccion: str
    jrv: str
    correlativo: str

# Leer el JSON desde un archivo
with open('datos.json') as file:
    data = json.load(file)

# Acceder a los datos
datos = data['datos']

posts = []
for registro in datos:
    post = Post(
        id=registro['id'],
        dui=registro['dui'],
        nombre=registro['nombre'],
        departamento=registro['departamento'],
        municipio=registro['municipio'],
        centro_de_votacion=registro['centro_de_votacion'],
        direccion=registro['direccion'],
        jrv=registro['jrv'],
        correlativo=registro['correlativo']
    )
    posts.append(post)



@app.get('/')
def read_root():
    return {"welcome": "Welcome to my REST API"}

@app.get('/posts')
def read_posts():
    return posts

@app.post("/posts")
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{id}')
def get_post(id: str):
    for post in posts:
        if post.id == id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# Ruta para obtener un post por DUI
@app.get('/posts/dui/{dui}', response_model=Post)
def read_post_by_dui(dui: str):
    for post in posts:
        if post.dui == dui:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post eliminado"}
    raise HTTPException(status_code=404, detail="Post Not found")

@app.put("/posts/{post_id}")
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
          posts[index]["title"] = updatedPost.title
          posts[index]["content"] = updatedPost.content
          posts[index]["author"] = updatedPost.author
          return {"message": "Post actualizado"}
    raise HTTPException(status_code=404, detail="Post Not found")
