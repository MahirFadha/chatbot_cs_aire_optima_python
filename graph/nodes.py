from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode

from graph.state import AgentState
from llm.gemini_client import get_llm
from tools.catalog_tools import tool_cari_katalog
from tools.order_tools import tool_tambah_pesanan
from tools.admin_tools import tool_panggil_admin

# 1. Masukkan alat ke sabuk perkakas
daftar_tools = [tool_cari_katalog, tool_tambah_pesanan, tool_panggil_admin]
node_eksekutor_alat = ToolNode(daftar_tools)

# 2. Siapkan Node Pemikir
def node_pemikir(state: AgentState):
    llm = get_llm().bind_tools(daftar_tools)
    
    # INI ADALAH JANTUNG DARI SUPER AGENT-MU
    sistem_prompt = f"""Kamu adalah Customer Service handal. Nomor HP pelanggan saat ini adalah {state['nomor_hp']}.
    SOP TOKO:
    1. Selalu ramah dan gunakan bahasa Indonesia yang baik.
    2. Jika ditanya harga/layanan, WAJIB gunakan `tool_cari_katalog`. Jangan pernah mengarang harga!
    3. Jika pelanggan mengonfirmasi pesanan (sudah tahu harga & alamat), gunakan `tool_tambah_pesanan`.
    4. Jika pelanggan marah, minta refund, atau ingin bicara dengan manusia, gunakan `tool_panggil_admin`.
    5. Jawablah pesan terakhir pengguna dengan natural berdasarkan data yang kamu dapatkan.
    """
    
    pesan_lengkap = [SystemMessage(content=sistem_prompt)] + state["messages"]
    
    # Suruh AI berpikir
    response = llm.invoke(pesan_lengkap)
    return {"messages": [response]}