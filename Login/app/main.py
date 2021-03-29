from typing import Optional
import uvicorn
from fastapi import FastAPI
import dns
# from routes.pulsa import *
from routes import pulsa, login
# from routes.pulsa import router as LoginRouter
# from routes.login import router as PulsaRouter

tags_metadata =[
    {"name": "login"},{"name": "pulsa"},
]

app = FastAPI(openapi_tags=tags_metadata)

# app.include_router(login.router, prefix="/login", tags=["Login !"],)
# app.include_router(pulsa.router, prefix="/pulsa", tags=["Pulsa !"],)
# app.include_router(LoginRouter, tags=["Login"], prefix="/login")
# app.include_router(PulsaRouter, tags=["Pulsa"], prefix="/pulsa")


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)


# # root endpoint
# @app.get("/")
# async def index():
#     return {"message": "Hello World"}

# # Endpoint Signup menggunakan metode POST


# @app.post("/signup/{email}/{username}/{password}")
# def signup(email, username: str, password: str):
#     user_exists = False
#     data = create_user(email, username, password)

#     # meng-convert data menjadi dict supaya lebih mudah di masukan ke mongodb
#     dict(data)

#     # mengecek apakah email tersebut sudah ada di collection users
#     if connection.db.users.find(
#         {'email': data['email']}
#     ).count() > 0:
#         user_exists = True
#         print("User Exists")
#         return {"message": "User Exists"}
#     # jika email belum ada, maka insert usert baru
#     elif user_exists == False:
#         connection.db.users.insert_one(data)
#         return {"message": "User Created", "email": data['email'], "name": data['name'], "pass": data['password']}

# # Login endpoint


# @app.get("/login/{email}/{password}")
# def login(email, password):
#     def log_user_in(creds):
#         if creds['email'] == email and creds['password'] == password:
#             return {"message": creds['name'] + ' successfully logged in'}
#         else:
#             return {"message": "Invalid credentials!!"}

#     # memvalidasi jika user sudah tersedia di dalam collection user dan mencocokan password
#     logger = check_login_creds(email, password)
#     if bool(logger) != True:
#         if logger == None:
#             logger = "Invalid Email"
#             return {"message": logger}
#     else:
#         status = log_user_in(logger)
#         return {"Info": status}


# @app.post("/master_pulsa/{kode_provider}/{nama_provider}/{harga_pokok}/{harga_jual}/{saldo}")
# def master_pulsa(kode_provider, nama_provider: str, harga_pokok: int, harga_jual: int, saldo: int):
#     provider_exists = False
#     pulsa = create_master_pulsa(
#         kode_provider, nama_provider, harga_pokok, harga_jual, saldo)

#     dict(pulsa)
#     if connection.db.master_pulsa.find(
#         {'kode_provider': pulsa['kode_provider']}
#     ).count() > 0:
#         provider_exists == True
#         print("Kode Provider Sudah Ada")
#         return {"message": "Kode Provider Sudah Ada"}
#     elif provider_exists == False:
#         connection.db.master_pulsa.insert_one(pulsa)
#         return{"message": "isi saldo awal master pulsa berhasil", "kode_provider": pulsa['kode_provider'], "nama_provider": pulsa['nama_provider'], "harga_pokok": pulsa['harga_pokok'], "harga_jual": pulsa['harga_jual'], "saldo": pulsa['saldo']}


# @app.get("/cek_all_provider")
# async def cek_all_provider():
#     col = connection.db["master_pulsa"]
#     for x in col.find():
#         print(x)
#         return print(x)

#     # cur = connection.db.master_pulsa.find()
#     # for dt in cur:
#     #     print(dt)
#     #     return{"kode provider": dt['kode_provider'], "nama provider": dt['nama_provider'], "harga pokok": dt['harga_pokok'], "harga jual": dt['harga_jual'], "saldo": dt['saldo']}
        

# @app.get("/cek_provider/{id}")
# async def cek_provider(id:str):
#     cur = connection.db.master_pulsa.find({"_id": ObjectId(id) })
#     try:
#         for dt in cur:
#             print(dt)
#             return{"kode provider": dt['kode_provider'], "nama provider": dt['nama_provider'], "harga pokok": dt['harga_pokok'], "harga jual": dt['harga_jual'], "saldo": dt['saldo']}
#     except Exception:
#         return {"message" : f"{id} tersebut tidak ada"}

# @app.delete("/{id}")
# async def hapus_transaksi_data(id: str):
#     col = connection.db['master_pulsa']
#     mq = {"_id" : ObjectId(id)}
#     col.delete_one(mq)
#     return {"message":f"ID kode provider {id} berhasil di hapus"}

# @app.put("/update_data_master_provider/{kode_provider}/{nama_provider}")
# async def update(kode_provider, nama_provider:str):
#     provider_exists = False

#     if connection.db.master_pulsa.find_one({'kode_provider' : kode_provider}):
#         col = connection.db["master_pulsa"]
#         lastquey = {'nama_provider' : nama_provider}
#         newquery = {"$set" : {'nama_provider' : nama_provider}}
#         col.update_one(lastquey, newquery)
#         for x in col.find():
#             print(x)
#             return {"message": f"nama provider dengan {id} berhasil di ubah"}
#     elif provider_exists == False:
#         return update

#     # if connection.db.master_pulsa.find_one({"_id": ObjectId(id)}).count() == 0:
#     #     col = connection.db["master_pulsa"]
#     #     lastquey = {'nama_provider' : nama_provider}
#     #     newquery = {"$set" : {'nama_provider' : nama_provider}}
#     #     col.update_one(lastquey, newquery)
#     #     for x in col.find():
#     #         print(x)
#     #         return {"message": f"nama provider dengan {id} berhasil di ubah"}
#     # else:
#     #     return {"message" : f"nama provider dengan {id} tidak terdaftar"}

