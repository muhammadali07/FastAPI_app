from typing import Optional
import uvicorn
from fastapi import FastAPI
import dns
from routes.pulsa import router as PulsaRouter
from routes.login import router as LoginRouter
from routes.transaksi import router as TransaksiRouter

app = FastAPI()

app.include_router(LoginRouter, tags=["Login"], prefix="/login")
app.include_router(PulsaRouter, tags=["Pulsa"], prefix="/pulsa")
app.include_router(TransaksiRouter, tags=["Transaksi"], prefix="/transaksi")

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)