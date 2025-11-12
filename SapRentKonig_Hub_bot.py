
# SapRentKonig_Hub_bot.py
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
import sqlite3
from datetime import datetime, timedelta
from docx import Document

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан. Добавьте переменную окружения BOT_TOKEN в Render")

RENTAL_NAME = "SapRentKonig_Hub"
OWNER_INFO = "Самозанятый Краснолобов Артем Александрович, +7 962 290-38-14"
TOTAL_BOARDS = 3
DB_FILE = "bookings.db"
CONTRACTS_DIR = "contracts"

if not os.path.exists(CONTRACTS_DIR):
    os.makedirs(CONTRACTS_DIR)

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    name TEXT,
    phone TEXT,
    passport_series_number TEXT,
    passport_issue_by TEXT,
    passport_issue_date TEXT,
    qty INTEGER,
    date TEXT,
    start_hour INTEGER,
    duration_hours INTEGER,
    contract_path TEXT
)""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привет! Это {RENTAL_NAME}. Используйте /booking чтобы забронировать SUP-борды.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используйте /booking чтобы начать бронирование.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_cmd))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
