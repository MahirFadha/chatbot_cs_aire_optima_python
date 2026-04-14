from langchain_core.tools import tool
from core.database import supabase
from llm.embedding_client import get_embedding_model

@tool
def tool_cari_katalog(kata_kunci: str) -> str:
    """Gunakan tool ini HANYA JIKA pelanggan bertanya harga produk (AC) atau layanan (Cuci AC/Pasang).
    PENTING: Gunakan kata_kunci yang panjang dan detail. (Misal: 'harga ac sharp 1 pk dan jasa pasang')"""
    try:
        print(f"\n[DEBUG TOOL] Gemini mulai mencari dengan kata kunci: '{kata_kunci}'")
        
        embedding_model = get_embedding_model()
        vektor_query = embedding_model.embed_query(kata_kunci)
        vektor_string = f"[{','.join(map(str, vektor_query))}]"
        
        # Eksekusi pencarian vektor di Supabase
        response = supabase.rpc(
            "match_documents", 
            {"query_embedding": vektor_string, "match_count": 5}
        ).execute()
        
        data = response.data
        if not data:
            print("[DEBUG TOOL] Hasil: Kosong / Tidak Ditemukan")
            return f"Maaf, tidak ditemukan data di katalog untuk '{kata_kunci}'."
            
        hasil_teks = "DATA KATALOG DITEMUKAN:\n"
        for item in data:
            hasil_teks += f"- {item.get('content')}\n"
            
        print(f"[DEBUG TOOL] Hasil sukses dikembalikan ke Gemini!")
        return hasil_teks
        
    except Exception as e:
        # INI CCTV PALING PENTING
        print(f"\n[ERROR FATAL TOOL KATALOG]: {e}\n")
        return f"Database error: {str(e)}"