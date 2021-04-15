from fastapi import APIRouter
import connection

router = APIRouter()

router.post("/jual_pulsa/{nama_provider}/{nominal}", tags=["Transaksi"])
def jual_pulsa(nama_provider, nominal:int):
    return ""
