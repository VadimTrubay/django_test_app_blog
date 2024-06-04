import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')


async def start(update: Update, context: CallbackContext) -> None:
    """
    The start function is the first function that will be called when a user
    sends a message to the bot. It sends back a welcome message and explains how
    to use the bot.
    
    :param update: Update: Get the update object
    :param context: CallbackContext: Access the context of the message
    :return: None, so the return type is none
    :doc-author: Trelent
    """
    await update.message.reply_text('Welcome! Use /help to see available commands.')


async def help_command(update: Update, context: CallbackContext) -> None:
    """
    The help_command function is a command handler that responds to the /help command.
    It sends a message with all available commands and their descriptions.
    
    :param update: Update: Get the update object, which contains all the information about the message
    :param context: CallbackContext: Pass the context of the update
    :return: A string with a list of commands
    :doc-author: Trelent
    """
    await update.message.reply_text('/start - Welcome message'
                                    '\n/help - List of commands'
                                    '\n/latest - Get the latest article'
                                    '\n/subscribe - Subscribe to updates')


async def latest(update: Update, context: CallbackContext) -> None:
    """
    The latest function retrieves the latest article from the API and sends it to the user.
    
    :param update: Update: Pass the update object to the function
    :param context: CallbackContext: Pass the context of the update
    :return: The latest article from the api
    :doc-author: Trelent
    """
    response = requests.get(f'{API_URL}latest-article/')
    if response.status_code == 200:
        article = response.json()[0]
        title = article['title']
        content = article['content']
        await update.message.reply_text(f"Latest Article:\n\nTitle: {title}\n\n{content}")
    else:
        await update.message.reply_text('Could not retrieve the latest article.')


async def subscribe(update: Update, context: CallbackContext) -> None:
    """
    The subscribe function subscribes the user to updates.
        Args:
            update (Update): The Telegram Update object.
            context (CallbackContext): The Telegram CallbackContext object.
    
    :param update: Update: Get the update object from the callback
    :param context: CallbackContext: Pass the context of the function
    :return: None, so it is not awaited
    :doc-author: Trelent
    """
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
