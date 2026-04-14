from langchain_core.tools import tool
from core.database import supabase # <-- Import koneksi Supabase kita

@tool
def tool_tambah_pesanan(nomor_hp: str, nama_produk: str, harga_total: int, alamat: str) -> str:
    """Gunakan tool ini JIKA pelanggan sudah setuju untuk memesan/order.
    Masukkan data pesanan ke dalam database."""
    try:
        order_data = {
            "produk": nama_produk, 
            "harga": harga_total, 
            "alamat": alamat
        }
        
        # Fitur upsert akan otomatis Insert jika nomor baru, atau Update jika nomor sudah ada
        # Menembak schema 'public' tabel 'users'
        response = supabase.table("users").upsert({
            "phone_number": nomor_hp,
            "order_temp": order_data
        }).execute()
        
        return "Pesanan berhasil disimpan ke keranjang database."
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR DB] {error_msg}")
        return f"Gagal menyimpan pesanan karena error sistem database."