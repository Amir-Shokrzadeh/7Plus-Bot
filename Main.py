import logging
import os
import time
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Sheet setup
def get_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(os.getenv("SHEET_URL")).sheet1
        data = sheet.get_all_values()
        return data
    except Exception as e:
        logger.error(f"Google Sheet error: {e}")
        return []

# Bot command

def start(update: telegram.Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 سلام! به 7Plus Academy خوش اومدی! هر روز یه نکته آیلتس اینجاست 💡")

def daily_tip(update: telegram.Update, context: CallbackContext) -> None:
    data = get_sheet_data()
    if not data:
        update.message.reply_text("خطا در بارگیری نکات. لطفاً بعداً تلاش کنید.")
        return

    import random
    tip = random.choice(data)
    if tip:
        text = f"📌 IELTS Tip of the Day:\n\n{tip[0]}\n\n🇮🇷 {tip[1]}"
        update.message.reply_text(text)

# Main
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tip", daily_tip))

    updater.start_polling()
    updater.idle()
