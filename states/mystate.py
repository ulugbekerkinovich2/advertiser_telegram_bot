from aiogram.dispatcher.filters.state import StatesGroup, State



class User(StatesGroup):
    get_command = State()
    send_message = State()
    image = State()
    text = State()
    reklama_admin_image_all = State()
    reklama_admin_image_text_for_admins = State()
    reklama_admin_video_or_image_all = State()