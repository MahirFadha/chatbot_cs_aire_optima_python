from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY

def get_llm():
    # Kamu bisa ubah ke model flash untuk kecepatan
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        api_key=GEMINI_API_KEY,
        temperature=0.3 # Sedikit kaku agar tidak mengarang harga
    )