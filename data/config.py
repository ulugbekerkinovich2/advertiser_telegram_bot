from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
import os
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
admins_str = os.environ.get("ADMINS", "")
# Split the string by comma and convert each part to an integer
admin_ids = [int(admin_id) for admin_id in admins_str.split(",") if admin_id.strip()]
