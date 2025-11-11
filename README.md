# PROMPT

Vous avez dit :
tu es un developpeur backend expérimenté en python. je veux développer une API REST de gestion de users afin de tester un testeur débutant en API. l'API doit me permettre de créer, modifier (partiellement et totalement, récupérer et supprimer un user. l'échange de données doit être en JSON. l'authetification doit être via un username et un mot de passe.
peux tu me développer cet API et me fournir une documentation sous format de swagger qui présentra tous les champs obligatoire et optionnelle avec leur types ainsi que les codes de retour attendu.
ChatGPT a dit :
Excellent projet — parfait pour tester un testeur API débutant 👏
On va construire une API REST complète de gestion d’utilisateurs avec FastAPI, car c’est rapide à mettre en place, parfaitement adapté à Python et génère automatiquement la documentation Swagger (OpenAPI).

⚙️ Objectif
Créer une API permettant de :

🔹 Créer un utilisateur (POST /users)

🔹 Récupérer la liste des utilisateurs (GET /users)

🔹 Récupérer un utilisateur spécifique (GET /users/{user_id})

🔹 Modifier un utilisateur totalement (PUT /users/{user_id})

🔹 Modifier un utilisateur partiellement (PATCH /users/{user_id})

🔹 Supprimer un utilisateur (DELETE /users/{user_id})

🔐 Authentification basique via username / password

Les échanges se feront en JSON.

🧠 Stack technique
Langage : Python 3.10+

Framework : FastAPI

Authentification : Basic Auth

Stockage : En mémoire (dict) pour simplifier le test

📁 Structure du projet
user_api/
├── main.py
├── models.py
├── auth.py
└── requirements.txt
📦 requirements.txt
fastapi
uvicorn
pydantic
🧩 models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="secret123")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.new@example.com")
    full_name: Optional[str] = Field(None, example="John New")
    password: Optional[str] = Field(None, min_length=6, example="newpass123")

class User(UserBase):
    id: int
🔐 auth.py
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Exemple d'utilisateur admin pour l'authentification basique
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
🚀 main.py
from fastapi import FastAPI, HTTPException, status, Depends
from typing import Dict
from models import User, UserCreate, UserUpdate
from auth import authenticate

app = FastAPI(
    title="User Management API",
    description="Une API REST pour gérer les utilisateurs (CRUD) avec authentification basique.",
    version="1.0.0",
)

# Stockage en mémoire
users_db: Dict[int, User] = {}
next_id = 1

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, username: str = Depends(authenticate)):
    global next_id
    new_user = User(id=next_id, **user.dict(exclude={"password"}))
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@app.get("/users", response_model=list[User])
def list_users(username: str = Depends(authenticate)):
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, username: str = Depends(authenticate)):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate, username: str = Depends(authenticate)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = User(id=user_id, **updated_user.dict(exclude={"password"}))
    users_db[user_id] = user
    return user

@app.patch("/users/{user_id}", response_model=User)
def partial_update_user(user_id: int, updated_fields: UserUpdate, username: str = Depends(authenticate)):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = updated_fields.dict(exclude_unset=True)
    user_data = user.dict()
    user_data.update(updated_data)
    updated_user = User(**user_data)
    users_db[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, username: str = Depends(authenticate)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None
🧭 Lancer l’API
uvicorn main:app --reload
🌐 Accès à la documentation Swagger
Ouvre ton navigateur à l’adresse :
👉 http://127.0.0.1:8000/docs

Tu auras une documentation interactive complète avec tous les champs, leurs types, et les codes de retour (générés automatiquement via OpenAPI/Swagger).

🧾 Résumé des Endpoints
Méthode	Endpoint	Description	Auth requise	Corps attendu	Codes de retour
POST	/users	Créer un utilisateur	✅	UserCreate	201, 401
GET	/users	Lister tous les utilisateurs	✅	—	200, 401
GET	/users/{id}	Récupérer un utilisateur	✅	—	200, 404, 401
PUT	/users/{id}	Mise à jour complète	✅	UserCreate	200, 404, 401
PATCH	/users/{id}	Mise à jour partielle	✅	UserUpdate	200, 404, 401
DELETE	/users/{id}	Supprimer un utilisateur	✅	—	204, 404, 401
Souhaites-tu que je te génère un fichier YAML Swagger complet (openapi.yaml) à importer dans Postman ou Swagger Editor ?
Je peux te le produire à partir du code ci-dessus.




Aucun fichier choisiAucun fichier choisi
ChatGPT peut commettre des erreurs. Il est recommandé de vérifier les informations importantes. Voir les préférences en matière de cookies.
