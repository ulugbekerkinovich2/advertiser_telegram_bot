import requests
from icecream import ic


def save_chat_id(chat_id,firstname, lastname,bot_id,username,status):
    url = "https://space.misterdev.uz/users/post"
    data = {
        "chat_id": chat_id,
        "firstname": firstname if firstname else "firstname not found",
        "lastname": lastname if lastname else "lastname not found",
        "bot_id": bot_id,
        "username": username if username else "username not found",
        "status": status
        }
    ic(data)
    response = requests.post(url, json=data)
    
    return response.json()

def update_user(id, chat_id,firstname, lastname,bot_id,username,status,created_at):
    url = f"https://space.misterdev.uz/users/put/{id}"
    data = {
        "chat_id": chat_id,
        "firstname": firstname if firstname else "firstname not found",
        "lastname": lastname if lastname else "lastname not found",
        "bot_id": bot_id,
        "username": username if username else "username not found",
        "status": status,
        'created_at': created_at
        }
    ic(data)
    response = requests.put(url, json=data)
    return response.json()

def get_all_bots():
    url = "https://space.misterdev.uz/bots/get"
    response = requests.get(url)
    return response.json()

def get_all_users():
    url = "https://space.misterdev.uz/users/get"
    response = requests.get(url)
    
    return response.json()


