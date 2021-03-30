from schematics.models import Model
from bson import ObjectId
from schematics.types import StringType, EmailType, NumberType, TimestampType
import connection

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


def provider_exists(kode_provider, nama_provider):
    provider_exists = True
    if connection.db.master_pulsa.find({"$or":[{'kode_provider': kode_provider}, {'nama_provider':nama_provider}]}
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

