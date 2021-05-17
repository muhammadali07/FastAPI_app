from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.models_pulsa import *
from bson.json_util import dumps, loads
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
    output = []
    for x in col.find({}):
        output.append({"kode provider": x['kode_provider'], "nama provider": x['nama_provider'], "harga pokok": x['harga_pokok'], "harga jual": x['harga_jual'], "saldo": x['saldo']})
        json_data = dumps(output, indent = 2)
        with open('data.json', 'w') as file:
            file.write(json_data)
    return JSONResponse({'result' : output})
      
@router.get("/cek_provider_id/{id}", tags=["Pulsa"])
async def cek_provider_id(id:str):
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

@router.put("/update_data_master_provider_id/{id}/{nama_provider}/{harga_pokok}/{harga_jual}/{saldo}", tags=["Pulsa"])
async def update_data_master_provider_id(id:str, nama_provider:str,harga_pokok:int,harga_jual:int, saldo:int):
    try:
        if connection.db.master_pulsa.find_one({"_id":ObjectId(id)}):
            if connection.db.master_pulsa.find_one({"nama_provider":nama_provider}):
                return {"message" : f"nama provider tersebut sudah tersedia dengan kode berbeda"}
            else :
                connection.db.master_pulsa.find_one({"_id" : ObjectId(id)})
                db = connection.db.master_pulsa.update_one({"_id":ObjectId(id)}, {"$set":{"nama_provider":nama_provider, "harga_pokok":harga_pokok, "harga_jual":harga_jual, "saldo":saldo}})
                return {"message": f"Data provider dengan {id} berhasil diubah"}
        else:
            return {f"{id} tidak ditemukan"}
    except Exception:
        return update_data_master_provider_id


