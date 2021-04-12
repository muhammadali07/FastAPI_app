from fastapi import APIRouter
from models.models_pulsa import *
import connection

router = APIRouter()

@router.post("/master_pulsa/{kode_provider}/{nama_provider}/{harga_pokok}/{harga_jual}/{saldo}", tags=["Pulsa"])
def master_pulsa(kode_provider, nama_provider: str, harga_pokok: int, harga_jual: int, saldo: int):
    provider_exists = False
    pulsa = create_master_pulsa(
        kode_provider, nama_provider, harga_pokok, harga_jual, saldo)

    dict(pulsa)
    if connection.db.master_pulsa.find(
        {'kode_provider': pulsa['kode_provider']}
    ).count() > 0:
        provider_exists == True
        print("Kode Provider Sudah Ada")
        return {"message": "Kode Provider Sudah Ada"}
    elif provider_exists == False:
        connection.db.master_pulsa.insert_one(pulsa)
        return{"message": "isi saldo awal master pulsa berhasil", "kode_provider": pulsa['kode_provider'], "nama_provider": pulsa['nama_provider'], "harga_pokok": pulsa['harga_pokok'], "harga_jual": pulsa['harga_jual'], "saldo": pulsa['saldo']}


@router.get("/cek_all_provider", tags=["Pulsa"])
async def cek_all_provider():
    col = connection.db.master_pulsa
    # return list(col.find({}))
    for x in col.find({}):
        print(x)
    
@router.get("/cek_provider/{id}", tags=["Pulsa"])
async def cek_provider(id:str):
    cur = connection.db.master_pulsa.find({"_id": ObjectId(id) })
    try:
        for dt in cur:
            print(dt)
            return{"kode provider": dt['kode_provider'], "nama provider": dt['nama_provider'], "harga pokok": dt['harga_pokok'], "harga jual": dt['harga_jual'], "saldo": dt['saldo']}
    except Exception:
        return {"message" : f"{id} tersebut tidak ada"}

@router.delete("/detele_transaction/{id}", tags=["Pulsa"])
async def hapus_transaksi_data(id: str):
    col = connection.db['master_pulsa']
    mq = {"_id" : ObjectId(id)}
    col.delete_one(mq)
    return {"message":f"ID kode provider {id} berhasil di hapus"}

@router.put("/update_data_master_provider/{id}/{nama_provider}", tags=["Pulsa"])
async def update_data_master_provider(id, nama_provider:str):
    try:
        if connection.db.master_pulsa.find_one({"_id" : ObjectId(id)}):
            raise Exception
            db = connection.db["pulsa"]
            col = db["master_pulsa"]
            last_nama_provider = {"nama_provider" : nama_provider}
            new_nama_provider = {"$set" : {"nama_provider" : new_nama_provider}}
            col.update_one(last_nama_provider, new_nama_provider)
            for x in db.find():
                print(x)
                return {"message": "nama provider dengan {id} berhasil diubah"}
        else:
            return {"{id} tidak di temukan"}
    except Exception:
        return update_data_master_provider


