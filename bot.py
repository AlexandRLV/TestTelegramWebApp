from telegram import Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultGame
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, InlineQueryHandler
import json


JSON_NAME = "bot-info.json"
API_KEY = "7362459748:AAFyu1aRujXdxzmkY41K1NX0zk3-0WxyzXg"
GAME_URL = "https://game.rariaden-hub.ru/?v=1.0.3"
GAME_SHORT_NAME = "ZombieShooter"


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[KeyboardButton("Open Web App", web_app=WebAppInfo(url=GAME_URL))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text('Откройте веб-приложение', reply_markup=reply_markup)


async def game(update: Update, context: CallbackContext) -> None:
    await update.get_bot().send_game(chat_id=update.message.chat_id, game_short_name=GAME_SHORT_NAME)


async def game_inline(update: Update, context: CallbackContext) -> None:
    query_id = update.inline_query.id
    results = [InlineQueryResultGame(id = 1, game_short_name=GAME_SHORT_NAME)]
    await context.bot.answer_inline_query(inline_query_id=query_id, results=results)


async def handle_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Умею реагировать на команды /start, /app и /game')
        

async def handle_web_app_data(update: Update, context: CallbackContext) -> None:
    if update.message.web_app_data:
        received_data = update.message.web_app_data.data
        await update.message.reply_text(f'Вы отправили: {received_data}')
    else:
        await update.message.reply_text(f'Умею реагировать на команды /start и /app')


async def play_game(update: Update, context: CallbackContext) -> None:
    with open(JSON_NAME, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    game_url = data["game_url"] + "?v=" + data["game_version"]
    
    query = update.callback_query
    if query.game_short_name == GAME_SHORT_NAME:
        await context.bot.answer_callback_query(callback_query_id=query.id, url=game_url)
    else:
        await context.bot.answer_callback_query(callback_query_id=query.id, text="EMPTY")


def main():
    with open(JSON_NAME, 'r', encoding='utf-8') as file:
        data = json.load(file)

    print('starting tg game bot with settings:')
    print(data)

    API_KEY = data["api_key"]
    GAME_URL = data["game_url"] + "?v=" + data["game_version"]
    GAME_SHORT_NAME = data["game_name"]

    print('api key:' + API_KEY)
    print('url:' + GAME_URL)
    print('name:' + GAME_SHORT_NAME)

    application = Application.builder().token(API_KEY).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('app', start))
    application.add_handler(CommandHandler('game', game))
    application.add_handler(InlineQueryHandler(game_inline))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    application.add_handler(CallbackQueryHandler(play_game))

    application.run_polling()


if __name__ == '__main__':
    main()
