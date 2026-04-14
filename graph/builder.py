from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import AgentState
from graph.nodes import node_pemikir, node_eksekutor_alat

def polisi_cek_kebutuhan_alat(state: AgentState):
    """Mengecek apakah AI butuh pakai alat atau tidak."""
    pesan_terakhir = state["messages"][-1]
    if pesan_terakhir.tool_calls:
        return "ke_alat"
    return "selesai"

def rakit_super_agent():
    pabrik = StateGraph(AgentState)
    
    pabrik.add_node("ruang_pemikir", node_pemikir)
    pabrik.add_node("ruang_tools", node_eksekutor_alat)
    
    pabrik.add_edge(START, "ruang_pemikir")
    
    pabrik.add_conditional_edges(
        "ruang_pemikir", 
        polisi_cek_kebutuhan_alat,
        {"ke_alat": "ruang_tools", "selesai": END}
    )
    
    pabrik.add_edge("ruang_tools", "ruang_pemikir")
    
    cctv_memori = MemorySaver() # Simpan chat memory
    return pabrik.compile(checkpointer=cctv_memori)

# Kita buat 1 instansiasi agent global agar memorinya bertahan selama server menyala
SUPER_AGENT = rakit_super_agent()