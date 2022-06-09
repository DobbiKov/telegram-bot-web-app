from importlib.resources import contents
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from data.config import BOT_TOKEN

from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiohttp.web_app import Application

#
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.content_types import ContentTypesFilter, ContentType

from aiogram import Bot
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiohttp.web import run_app

from routes import check_data_handler, send_message_handler
from aiogram.dispatcher.filters import Command

TOKEN = BOT_TOKEN
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
my_router = Router()

logger = logging.getLogger(__name__)

@my_router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard= [[
            InlineKeyboardButton(text="Google", web_app=WebAppInfo(url="https://cumpbotweb.dobbikov.com/"))
        ]]
    )
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard = [[
            KeyboardButton(text = "Подати заявку", web_app = WebAppInfo(url="https://cumpbotweb.dobbikov.com/"))
        ]]
    )
    await message.answer(f"Привіт, {message.from_user.full_name}!", reply_markup=reply_keyboard)

@my_router.message(ContentTypesFilter(content_types=[ContentType.WEB_APP_DATA]))
async def web_app_handler(message: types.Message) -> None:
    # print(message.web_app_data)
    # print("remove it!!")
    print(message.web_app_data.data)
    data = json.loads(message.web_app_data.data)
    print(data["name"])
    print(data["email"])
    print(data["discord"])
    print(data["nickname"])
    print(data["age"])

    name = data["name"]
    email = data["email"]
    discord = data["discord"]
    nickname = data["nickname"]
    age = data["age"]

    await bot.send_message(
        -1001768046932, 
        f"<a href='tg://user?id={message.from_user.id}'>{name}</a> надіслав заявку:\n\n\
Email: <b>{email}</b>\n\
Discord: <b>{discord}</b>\n\
Nickname: <b>{nickname}</b>\n\
Вік: <b>{age}</b>\n\
", parse_mode="HTML")
    await bot.send_message(message.from_user.id, "Дякуємо за надіслану заявку!\nМи її отримали та відповімо вам, коли її перевіримо.\nГарного дня!")



    # message.answer("{message.web_app_data.data}")

@my_router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender
    By default message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
    



async def on_startup(bot: Bot, base_url: str):
    # dp.register_message(command_start_handler, commands=['start'])
    # Router.register_message(command_start_handler, commands=['start'])
    webhook = await bot.get_webhook_info()

    WEBHOOK_URL = f"https://cumpbot.dobbikov.com/webhook"

    # If URL is bad
    if webhook.url != WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(WEBHOOK_URL)
        # If you want to use free certificate signed by LetsEncrypt you need to set only URL without sending certificate.


    # await bot.set_webhook(f"{base_url}/webhook")
    # await bot.set_chat_menu_button(
    #     menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"https://cumpbotweb.dobbikov.com/"))
    # )

def main() -> None:
    # Initialize Bot instance with an default parse mode which will be passed to all API calls
    # bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    # dp.run_polling(bot)

    dispatcher = Dispatcher()
    dispatcher["base_url"] = f"https://cumpbot.dobbikov.com"
    dispatcher.startup.register(on_startup)

    dispatcher.include_router(my_router)

    app = Application()
    app["bot"] = bot
    # app.router.add_get("/demo", demo_handler)
    # app.router.add_post("/demo/checkData", check_data_handler)
    # app.router.add_post("/demo/sendMessage", send_message_handler)
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path="/webhook")
    setup_application(app, dispatcher, bot=bot)

    run_app(app, host="127.0.0.1", port=3003)

if __name__ == "__main__":
    main()