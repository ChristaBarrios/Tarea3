import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Creación de una instancia FastAPI
app = FastAPI()

# Diccionario para almacenar los usuarios, donde la clave es el ID de usuario y el valor es un objeto User.
users_dict = {}


# Definición de la clase User para representar la información del usuario
class User(BaseModel):
    user_name: str  # Nombre del usuario
    user_id: int  # ID único del usuario
    user_email: str  # Correo electrónico del usuario
    age: int = None  # Edad del usuario (opcional, puede ser None)
    recommendations: list = []  # Lista de recomendaciones para el usuario (opcional, lista vacía por defecto)
    ZIP: int = None  # Código postal del usuario (opcional, puede ser None)


# Endpoint para crear un nuevo usuario con un ID único
@app.post("/create_user/")
async def create_user(user: User):
    user_id = user.user_id
    if user_id in users_dict:
        raise HTTPException(status_code=400, detail="El ID de usuario ya existe")
    users_dict[user_id] = user
    return {"user_id": user_id, "message": "Usuario creado exitosamente"}


# Endpoint para actualizar información de un usuario por su ID
@app.put("/update_user/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id not in users_dict:
        raise HTTPException(status_code=404, detail="El ID de usuario no existe")
    users_dict[user_id] = user
    return {"user_id": user_id, "message": "Usuario actualizado exitosamente"}


# Endpoint para obtener información de un usuario por su ID
@app.get("/get_user/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_dict:
        raise HTTPException(status_code=404, detail="El ID de usuario no existe")
    user = users_dict[user_id]
    return user


# Endpoint para eliminar información de un usuario por su ID
@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_dict:
        raise HTTPException(status_code=404, detail="El ID de usuario no existe")
    del users_dict[user_id]
    return {"message": "Usuario eliminado exitosamente"}


# Iniciar la aplicación FastAPI usando uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=False)
