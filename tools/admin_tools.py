from langchain_core.tools import tool
from core.waha import waha_send_text

@tool
def tool_panggil_admin(alasan: str, nomor_hp_pelanggan: str) -> str:
    """Gunakan tool ini JIKA pelanggan marah, komplain, atau meminta disambungkan dengan Admin Manusia.
    Jangan gunakan tool ini untuk ngobrol biasa."""
    
    NOMOR_ADMIN = "62812xxxxxx"  # Ganti dengan nomor WA Admin-mu
    pesan_notif = f"🚨 NOTIFIKASI ADMIN!\nPelanggan ({nomor_hp_pelanggan}) butuh bantuan.\nAlasan: {alasan}"
    
    # Kirim pesan ke HP Admin
    waha_send_text(NOMOR_ADMIN, pesan_notif)
    
    return "Pesan sudah dikirim ke Admin. Beritahu pelanggan bahwa admin akan segera merespons."