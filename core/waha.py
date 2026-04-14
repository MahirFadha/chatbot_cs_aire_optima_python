import requests
from config.settings import WAHA_API_URL, WAHA_API_KEY # Tambahkan import key

def waha_send_typing(chat_id: str):
    """Menampilkan status 'Sedang mengetik...' di HP pelanggan"""
    url = f"{WAHA_API_URL}/api/startTyping"
    payload = {
        "session": "default", 
        "chatId": chat_id
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        pass

def waha_send_text(chat_id: str, text: str):
    url = f"{WAHA_API_URL}/api/sendText"
    headers = {
        "X-Api-Key": WAHA_API_KEY  # WAHA membutuhkan ini jika security aktif
    }
    payload = {
        "session": "default", 
        "chatId": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"[WAHA RESPONSE]: {response.text}")