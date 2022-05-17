import json
import yt_dlp

import logging
import constant
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def info(update: Update, context: CallbackContext):
    url = context.args[0]
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info_fix = ydl.sanitize_info(info)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=info_fix["title"])


if __name__ == '__main__':
    application = ApplicationBuilder().token(constant.bot_token).build()
   
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    info_handler = CommandHandler('info',info)
    
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(echo_handler)
    application.add_handler(info_handler)
    application.run_polling()
