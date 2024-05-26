from telegram import Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


API_KEY = "7362459748:AAFyu1aRujXdxzmkY41K1NX0zk3-0WxyzXg"
APP_URL = "https://alexandrlv.github.io/TestTelegramWebApp/index.html"


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[KeyboardButton("Open Web App", web_app=WebAppInfo(url=APP_URL))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text('Откройте веб-приложение', reply_markup=reply_markup)

async def handle_web_app_data(update: Update, context: CallbackContext) -> None:
    if update.message.web_app_data:
        received_data = update.message.web_app_data.data
        await update.message.reply_text(f'Вы отправили: {received_data}')
    else:
        await update.message.reply_text(f'Умею реагировать на команды /start и /app')

def main():
    application = Application.builder().token(API_KEY).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('app', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_web_app_data))

    application.run_polling()


if __name__ == '__main__':
    main()
