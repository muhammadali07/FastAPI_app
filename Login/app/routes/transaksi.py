from fastapi import APIRouter
from models.models_pulsa import *
import connection

router = APIRouter()

@router.post("/jual_pulsa/{kode_provider}/{qty_pulsa}", tags=["Transaksi"])
def jual_pulsa(kode_provider:str, qty_pulsa:int):
    try:
        if connection.db.master_pulsa.find_one({"kode_provider": kode_provider}):
            nama_provider = connection.db.master_pulsa.find_one({"kode_provider":kode_provider})
            print(nama_provider)
            connection.db.transaksi_pulsa.insert_one({"kode_provider":kode_provider, "nama_provider":nama_provider, "qty_pulsa":qty_pulsa})
            return {"message":f"transaksi pulsa provider {kode_provider} berhasil"}
        else:
            return {"message":f"Kode Provider {kode_provider} tidak tersedia"}
    except Exception:
        return jual_pulsa