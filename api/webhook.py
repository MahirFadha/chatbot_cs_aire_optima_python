from graph.builder import SUPER_AGENT
from fastapi import APIRouter, Request, BackgroundTasks
from core.database import supabase # <-- Import koneksi Supabase kita
from core.waha import waha_send_text, waha_send_typing

router = APIRouter()

def is_blacklisted(text: str) -> bool:
    """Mengecek tabel blacklisted_words di schema 'public' menggunakan API Supabase"""
    try:
        # Mengambil data dari schema 'public', tabel 'blacklisted_words'
        response = supabase.table("blacklisted_words").select("word").execute()
        
        # Ekstrak data kata dari JSON response
        bad_words = [row['word'].lower() for row in response.data]
        
        text_lower = text.lower()
        for bw in bad_words:
            if bw in text_lower:
                return True
        return False
    except Exception as e:
        print(f"Error cek blacklist Supabase: {e}")
        return False

def proses_pesan_background(chat_id: str, text: str):
    waha_send_typing(chat_id)
    
    if is_blacklisted(text):
        waha_send_text(chat_id, "Mohon maaf, pesan Anda mengandung kata yang tidak pantas.")
        return 

    print(f"\n[SISTEM] Membangunkan Super Agent untuk {chat_id}...")
    
    try:
        # Gunakan nomor HP sebagai ID Sesi Memori (KTP)
        config = {"configurable": {"thread_id": chat_id}}
        
        # Kirim Pesan dan Nomor HP ke Papan Jalan awal LangGraph
        input_state = {
            "messages": [("user", text)],
            "nomor_hp": chat_id
        }
        
        # Jalankan mesin!
        hasil_akhir = SUPER_AGENT.invoke(input_state, config=config)
        
        # Ambil jawaban AI
        isi_pesan = hasil_akhir["messages"][-1].content
        
        # Bersihkan signature Gemini jika berbentuk list (seperti yang kita bahas sebelumnya)
        if isinstance(isi_pesan, list):
            jawaban_ai = "".join(item.get("text", "") for item in isi_pesan if isinstance(item, dict))
        else:
            jawaban_ai = isi_pesan
            
        waha_send_text(chat_id, jawaban_ai)
        
    except Exception as e:
        print(f"Error Eksekusi LangGraph: {e}")
        waha_send_text(chat_id, "Maaf, sistem kami sedang mengalami gangguan. Mohon tunggu sebentar.")


@router.post("/waha-webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    """Menerima lemparan data JSON dari WAHA"""
    data = await request.json()

    print("\n--- DATA MASUK DARI WAHA ---")
    print(data) 
    print("---------------------------\n")
    
    try:
        # Menyesuaikan dengan struktur payload WAHA
        payload = data.get("payload", {})
        
        # Hindari membalas pesan dari diri sendiri (bot)
        if payload.get("fromMe", False):
            return {"status": "ignored_from_me"}
            
        chat_id = payload.get("from", "")
        body = payload.get("body", "")
        
        # Jika bukan pesan teks biasa (misal: image/video), kita abaikan dulu
        if not body:
            return {"status": "ignored_no_text"}

        print(f"\n[WEBHOOK] Pesan baru dari {chat_id}: {body}")
        
        # Jalankan proses di background agar FastAPI langsung membalas "200 OK" ke WAHA
        background_tasks.add_task(proses_pesan_background, chat_id, body)
        
        return {"status": "success", "message": "Pesan sedang diproses AI"}

    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "detail": str(e)}