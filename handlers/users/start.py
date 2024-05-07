from aiogram import types, Bot
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
import asyncio
from states.mystate import User
from data.config import BOT_TOKEN,admin_ids
from utils import send_req
from filters.custom import IsAdminFilter
from icecream import ic
import datetime
# from telegram import ParseMode
# Your import statements are incomplete, so you may need to adjust these accordingly

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.from_user.id
    
    all_bots = send_req.get_all_bots()  # Assuming you get all bots from somewhere
    all_users = send_req.get_all_users()  # Assuming you get all users from somewhere
    
    if chat_id not in all_users:
        for bot in all_bots:
            if bot["api_key"] == BOT_TOKEN:  # Assuming BOT_TOKEN is defined somewhere
                bot_id = bot["id"]
                send_req.save_chat_id(chat_id, firstname, lastname, bot_id, username, 'active')  # Assuming you have a function like this
        await message.answer(f"Salom, {message.from_user.full_name}!")
    else:
        await message.answer(f"Siz uje borsiz, {message.from_user.full_name}!")








#TODO for all users
@dp.message_handler(text="/reklama_admin_text_for_all_users")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    await message.answer("Reklama xabarini yuboring, ushbu habar barcha user larga boradi!!!")
    await User.get_command.set()



@dp.message_handler(state=User.get_command)
async def bot_echo(message: types.Message, state: FSMContext):
    text = message.text  # Renamed to 'text' to avoid overwriting the 'message' variable
    ic(text)
    bot = Bot(token=BOT_TOKEN)  # Assuming BOT_TOKEN is defined somewhere
    all_users = send_req.get_all_users()  # Assuming you get all users from somewhere
    ic(all_users) # Assuming
    failed = 0
    count = 0
    for user_id in all_users:
        try:
            await bot.send_message(user_id['chat_id'], text, parse_mode=types.ParseMode.HTML)
            # Add a small delay to avoid being banned for spam
            await asyncio.sleep(0.1)
            count += 1
            send_req.update_user(user_id['id'], user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'active')
        except Exception as e:
            failed += 1 
            send_req.update_user(user_id['id'], user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'blocked')
            print(f"Failed to send message to user {user_id}: {e}")
    await state.finish()
    await message.reply(f"Reklama yuborildi! {count} ta userga, {failed} ta userga bormadi")
    








@dp.message_handler(text="/reklama_admin_image_all")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    await message.answer("Reklama rasmini matni bilan yuboring, ushbu habar barcha userlarga boradi")
    await User.reklama_admin_image_all.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT], state=User.reklama_admin_image_all)
async def handle_image_and_text(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.TEXT:
        
        # Handle text message
        text = message.text
        await process_text(message, text)

    elif message.content_type == types.ContentType.PHOTO:
        # Handle image message
        photo_file_id = message.photo[-1].file_id
        caption = message.caption
        await process_image(message, photo_file_id, caption, state)

async def process_image(message: types.Message, photo_file_id: str, caption: str, state: FSMContext):
    # Process the image message
    print("Photo file ID:", photo_file_id)
    print("Caption:", caption)

    bot = Bot(token=BOT_TOKEN)  # Assuming BOT_TOKEN is defined somewhere
    all_users = send_req.get_all_users()  # Assuming you get all users from somewhere
    failed = 0
    count = 0
    for user_info in all_users:
        user_id = user_info.get('chat_id')
        ic(user_id)
        try:
        # Parse the text as Markdown to make links clickable
            await bot.send_photo(user_id, photo=photo_file_id, caption=caption, parse_mode="HTML")
            
            # Add a small delay to avoid being banned for spam
            await asyncio.sleep(0.3)
            count += 1
            send_req.update_user(user_info['id'], user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'active')
        except Exception as e:
            failed += 1
            send_req.update_user(int(user_info.get('id')), user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'blocked',user_info['created_at'])
            print(f"Failed to send message to user {user_id}: {e}")

    await message.reply(f"Reklama yuborildi! {count}ta userga, {failed} ta userga bormadi")
    await state.finish()










@dp.message_handler(text="/reklama_admin_image_text_for_admins")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    await message.answer("Reklama rasmini yuboring, ushbu reklama adminlarga boradi")
    await User.reklama_admin_image_text_for_admins.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT], state=User.reklama_admin_image_text_for_admins)
async def handle_image_and_text(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.TEXT:

        text = message.text
        await process_text(message, text)

    elif message.content_type == types.ContentType.PHOTO:
        # Handle image message
        photo_file_id = message.photo[-1].file_id
        caption = message.caption
        await process_image1(message, photo_file_id, caption, state)

# async def process_text(message: types.Message, text: str):
#     # Process the text message
#     # print("Text:", text)
#     await message.answer(text)

async def process_image1(message: types.Message, photo_file_id: str, caption: str, state: FSMContext):
    # Process the image message
    # print("Photo file ID:", photo_file_id)
    # print("Caption:", caption)

    bot = Bot(token=BOT_TOKEN) # Assuming you get all users from somewhere
    fail_count = 0
    count = 0
    for user_id in admin_ids:
        ic(user_id)
        # user_id = user_info.get('chat_id')
        try:
            await bot.send_photo(user_id, photo=photo_file_id, caption=caption)
            # Add a small delay to avoid being banned for spam
            await asyncio.sleep(0.4)
            count += 1
            # send_req.update_user(user_id['id'], user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'active', user_id['created_at'])
        except Exception as e:
            fail_count += 1
            # send_req.update_user(int(user_id.get('id')), user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'blocked',user_id['created_at'])
            print(f"Failed to send message to user {user_id}: {e}")

    await message.reply(f"Reklama adminlarga yuborildi!, {count} ta adminga\nReklama adminlarga yuborilmadi, {fail_count} ta adminga")
    await state.finish()







#TODO video uchun
@dp.message_handler(text="/reklama_admin_video_or_image_all")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    await message.answer("Reklama videosini yuboring yoki rasmini matni, ushbu reklama hammaga boradi")
    await User.reklama_admin_video_or_image_all.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT], state=User.reklama_admin_video_or_image_all)
async def handle_media_and_text(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.TEXT:
        # Handle text message
        text = message.text
        await process_text(message, text)

    elif message.content_type in [types.ContentType.PHOTO, types.ContentType.VIDEO]:
        # Handle media message
        media_file_id = message.video.file_id if message.content_type == types.ContentType.VIDEO else message.photo[-1].file_id
        caption = message.caption
        await process_media(message, media_file_id, caption, state)

async def process_text(message: types.Message, text: str):
    # Process the text message
    print("Text:", text)
    await message.answer(text)

async def process_media(message: types.Message, media_file_id: str, caption: str, state: FSMContext):
    # Process the media message
    print("Media file ID:", media_file_id)
    print("Caption:", caption)

    bot = Bot(token=BOT_TOKEN)  # Assuming BOT_TOKEN is defined somewhere
    all_users = send_req.get_all_users()  # Assuming you get all users from somewhere
    failed = 0
    count = 0
    for user_info in all_users:
        ic(user_info)
        user_id = user_info.get('chat_id')
        try:
            if message.content_type == types.ContentType.PHOTO:
                await bot.send_photo(user_id, photo=media_file_id, caption=caption)
            elif message.content_type == types.ContentType.VIDEO:
                await bot.send_video(user_id, video=media_file_id, caption=caption)
            # Add a small delay to avoid being banned for spam
            await asyncio.sleep(0.1)
            count += 1
            
            send_req.update_user(user_info['id'], user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'active', user_info['created_at'])
        except Exception as e:
            failed += 1
            send_req.update_user(int(user_info.get('id')), user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'blocked',user_info['created_at'])
            print(f"Failed to send message to user {user_id}: {e}")

    await message.reply(f"Reklama yuborildi! {count}ta userga, {failed} ta userga yuborilmadi")
    await state.finish()

@dp.message_handler(text="/reklama_admin_statistika")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count_of_users = send_req.get_all_users()
    active = 0
    blocked = 0
    for user in count_of_users:
        if user['status'] == 'active':
            active += 1
        elif user['status'] == 'blocked':
            blocked += 1
    response_message = (
    f"Sana: {time}\n\n"
    f"Botda {len(count_of_users)} ta foydalanuvchi bor.\n\n"
    f"Aktiv: {active} ta foydalanuvchi.\n"
    f"Bloklangan: {blocked} ta foydalanuvchi."
)
    await message.answer(response_message)