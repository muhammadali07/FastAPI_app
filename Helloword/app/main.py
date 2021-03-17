from typing import Optional

from fastapi import FastAPI
import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType
import dns


class User(Model):
    user_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)
    password = StringType(required=True)

# Sebuah contoh dari pengguna kelas
newuser = User()

# funtion untuk membuat dan menetapkan nilai ke contoh kelas yang dibuat Pengguna
def create_user(email, username, password):
    newuser.user_id = ObjectId()
    newuser.email = email
    newuser.name = username
    newuser.password = password
    return dict(newuser)

# Metode untuk memeriksa apakah parameter email ada dari database pengguna sebelum validasi detail
def email_exists(email):
    user_exist = True

    # menghitung berapa kali email ada, jika sama dengan 0 berarti email tersebut tidak ada di database
    if connection.db.users.find(
        {'email': email}
    ).count() == 0:
        user_exist = False
        return user_exist

# membaca detail user dari database dan memvalidasi
def check_login_creds(email, password):
    if not email_exists(email):
        activeuser = connection.db.users.find(
            {'email': email}
        )
        for actuser in activeuser:
            actuser = dict(actuser)
            # Converted the user ObjectId to str! so this can be stored into a session(how login works)
            actuser['_id'] = str(actuser['_id'])    
            return actuser


app = FastAPI()




# root endpoint
@app.get("/")
async def index():
    return {"message": "Hello World"}

# Endpoint Signup menggunakan metode POST
@app.post("/signup/{email}/{username}/{password}")
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
        print("USer Exists")
        return {"message":"User Exists"}
    # jika email belum ada, maka insert usert baru
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password']}



# Login endpoint
@app.get("/login/{email}/{password}")
def login(email, password):
    def log_user_in(creds):
        if creds['email'] == email and creds['password'] == password:
            return {"message": creds['name'] + ' successfully logged in'}
        else:
            return {"message":"Invalid credentials!!"}

    # memvalidasi jika user sudah tersedia di dalam collection user dan mencocokan password
    logger = check_login_creds(email, password)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid Email"
            return {"message":logger}
    else:
        status = log_user_in(logger)
        return {"Info":status}