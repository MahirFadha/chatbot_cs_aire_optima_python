import uvicorn
from fastapi import FastAPI
from api.webhook import router as webhook_router

app = FastAPI(title="AI WAHA Super Agent")

# Daftarkan rute webhook
app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "Server AI WhatsApp Bot Sedang Menyala 🚀"}

if __name__ == "__main__":
    # Jalankan server di port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)