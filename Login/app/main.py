from typing import Optional

from fastapi import FastAPI
import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType, NumberType, TimestampType
import dns


class User(Model):
    user_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)
    password = StringType(required=True)

class MasterPulsa(Model):
    user_id = ObjectId()
    kode_provider = StringType(required=True)
    nama_provider = StringType(required=True)
    harga_pokok = NumberType(required =True)
    harga_jual = NumberType(required =True)
    saldo = NumberType(required = True)



# Sebuah contoh dari pengguna kelas
newuser = User()
newpulsa = MasterPulsa()

# funtion untuk membuat dan menetapkan nilai ke contoh kelas yang dibuat Pengguna
def create_user(email, username, password):
    newuser.user_id = ObjectId()
    newuser.email = email
    newuser.name = username
    newuser.password = password
    return dict(newuser)

def create_master_pulsa(kode_provider,nama_provider, harga_pokok, harga_jual, saldo):
    newpulsa.user_id = ObjectId()
    newpulsa.kode_provider = kode_provider
    newpulsa.nama_provider = nama_provider
    newpulsa.harga_pokok = harga_pokok
    newpulsa.harga_jual = harga_jual
    newpulsa.saldo = saldo
    return dict(newpulsa)

# Metode untuk memeriksa apakah parameter email ada dari database pengguna sebelum validasi detail
def email_exists(email):
    user_exist = True

    # menghitung berapa kali email ada, jika sama dengan 0 berarti email tersebut tidak ada di database
    if connection.db.users.find(
        {'email': email}
    ).count() == 0:
        user_exist = False
        return user_exist


def provider_exists(kode_provider):
    provider_exists = True
    if connection.db.master_pulsa.find(
        {'kode_provider': kode_provider}
    ).count() == 0:
        provider_exists = False
        return provider_exists


def transaction_exists(id):
    transaction_exists = True
    if connection.db.master_pulsa.find(
        {'id': id}
    ).count() == 0:
        transaction_exists = False
        return transaction_exists


# membaca detail user dari database dan memvalidasi
def check_login_creds(email, password):
    if not email_exists(email):
        activeuser = connection.db.users.find(
            {'email': email}
        )
        for actuser in activeuser:
            actuser = dict(actuser)
            # Mengonversi ObjectId pengguna menjadi str! jadi ini bisa disimpan ke dalam sesi (cara kerja login)
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
        print("User Exists")
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

@app.post("/master_pulsa/{kode_provider}/{nama_provider}/{harga_pokok}/{harga_jual}/{saldo}")
def master_pulsa(kode_provider,nama_provider:str,harga_pokok: int, harga_jual:int, saldo:int):
    provider_exists = False
    pulsa = create_master_pulsa(kode_provider,nama_provider, harga_pokok, harga_jual, saldo)

    dict(pulsa)
    if connection.db.master_pulsa.find(
        {'kode_provider': pulsa['kode_provider']}
        ).count() > 0:
        provider_exists == True
        print("Kode Provider Sudah Ada")
        return {"message" : "Kode Provider Sudah Ada"}
    elif provider_exists == False:
        connection.db.master_pulsa.insert_one(pulsa)
        return{"message" : "isi saldo awal master pulsa berhasil", "kode_provider": pulsa['kode_provider'],"nama_provider":pulsa['nama_provider'], "harga_pokok":pulsa['harga_pokok'],"harga_jual":pulsa['harga_jual'], "saldo": pulsa['saldo']}

@app.get("/cek_saldo_pulsa")
async def cek_saldo_pulsa():
    saldo = connection.db.master_pulsa.find()
    if saldo is None:
        print("Tidak ada data")
    else:
        print("cek saldo berhasil")
        return {saldo}

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
        
@app.delete("/{id}")
async def hapus_transaksi_data(id:str):
    if connection.db.master_pulsa.find(
        {'id': 'id'}
        ).count() > 0:
        transaction_exists == True
        connection.master_pulsa.delete_one({"id": ObjectId})
        return {"message" :"Transaksi dengan ID {id} berhasil di hapus"}
    elif transaction_exists == False:
        return {"message" :"Transaksi dengan ID {id} tidak ada"}
