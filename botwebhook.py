import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from currenyDatas import getCurrenciesMessage, loadData, makeMessageOne
from textChecking import checkForCurrencies
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv('TOKEN')
CURRENCIES = loadData()
print('Currencies are loaded')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html("Salom, men valyuta kurslari haqida ma'lumot berib boraman.\nShunchaki kerakli valyuta nomini yoki /all buyrug'ini yuboring. ")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

async def get_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(getCurrenciesMessage(CURRENCIES), parse_mode='html', disable_web_page_preview=True)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if c := checkForCurrencies(update.message.text):
        await update.message.reply_text(makeMessageOne(CURRENCIES[c]), parse_mode='html', disable_web_page_preview=True)


application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("all", get_all))

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app = Flask(__name__)

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), application.bot)
        return 'ok'
    else:
        return "<h1>Webhook ishlayapdi</h1>"

if __name__ == "__main__":
    application.bot.set_webhook("YOUR_PUBLIC_WEBHOOK_URL/webhook")
    app.run()