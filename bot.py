from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Contact
import logging


#relacionado a erros e excessões -
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



def cheat_response(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Você não passou nenhuma letra!')

def main():
    file_token = open("token.txt", "r")
    token = file_token.read().splitlines()
    file_token.close()

    updater = Updater(token=token[0] , use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("cheat", cheat_response))

    updater.start_polling()
    logging.info("=== Engines On! ===")

    updater.idle()
    logging.info("=== Turn off! === ")


if __name__ == '__main__':
    main()
