from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Riwayat pesan selalu ditambah ke bawah (append)
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Nomor HP disimpan di State agar Tool tahu siapa yang chat
    nomor_hp: str