from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("[SISTEM] Membangunkan Model Vektor...")
        _embedding_model = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-mpnet-base-v2"
        )
    return _embedding_model