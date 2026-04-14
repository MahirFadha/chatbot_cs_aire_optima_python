from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

# Inisialisasi Supabase Client secara global
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)