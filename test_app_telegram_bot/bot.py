import os
import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Use /help to see available commands.')


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('/start - Welcome message'
                                    '\n/help - List of commands'
                                    '\n/latest - Get the latest article'
                                    '\n/subscribe - Subscribe to updates')


async def latest(update: Update, context: CallbackContext) -> None:
    response = requests.get(f'{API_URL}latest-article/')
    if response.status_code == 200:
        article = response.json()[0]
        title = article['title']
        content = article['content']
        await update.message.reply_text(f"Latest Article:\n\nTitle: {title}\n\n{content}")
    else:
        await update.message.reply_text('Could not retrieve the latest article.')


async def subscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    response = requests.post(f'{API_URL}subscribe/', json={'chat_id': chat_id})
    if response.status_code == 201:
        await update.message.reply_text('You have been subscribed to updates.')
    else:
        await update.message.reply_text(response.json().get('status'))


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("latest", latest))
    application.add_handler(CommandHandler("subscribe", subscribe))

    application.run_polling()


if __name__ == '__main__':
    main()
