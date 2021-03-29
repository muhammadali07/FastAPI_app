from fastapi import APIRouter
from models.models_pulsa import *
import connection

router = APIRouter()

# root endpoint
@router.get("/",tags=["Login"])
async def index():
    return {"message": "Hello World"}

# Endpoint Signup menggunakan metode POST


@router.post("/signup/{email}/{username}/{password}", tags=["Login"])
def signup(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)

    # meng-convert data menjadi dict supaya lebih mudah di masukan ke mongodb
    dict(data)

    # mengecek apakah email tersebut sudah ada di collection users
    if connection.db.users.find(
        {'email': data['email']}
    ).count() > 0:
        user_exists = True
        print("User Exists")
        return {"message": "User Exists"}
    # jika email belum ada, maka insert usert baru
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {"message": "User Created", "email": data['email'], "name": data['name'], "pass": data['password']}

# Login endpoint


@router.get("/login/{email}/{password}", tags=["Login"])
def login(email, password):
    def log_user_in(creds):
        if creds['email'] == email and creds['password'] == password:
            return {"message": creds['name'] + ' successfully logged in'}
        else:
            return {"message": "Invalid credentials!!"}

    # memvalidasi jika user sudah tersedia di dalam collection user dan mencocokan password
    logger = check_login_creds(email, password)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid Email"
            return {"message": logger}
    else:
        status = log_user_in(logger)
        return {"Info": status}
