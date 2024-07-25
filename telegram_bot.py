from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sqlalchemy.orm import Session
import database
import notification_service
import employee_service
import datetime

API_TOKEN = "your_telegram_bot_token"
bot = Bot(token=API_TOKEN)
updater = Updater(token=API_TOKEN, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать! Вы будете получать уведомления о днях рождения.')

def notify_subscribers(context: CallbackContext):
    db = database.SessionLocal()
    today = datetime.date.today()
    employees = employee_service.get_employees(db)
    for employee in employees:
        if employee.birthday.month == today.month and employee.birthday.day == today.day:
            subscribers = notification_service.get_subscribers(db, employee.id)
            for subscriber in subscribers:
                context.bot.send_message(chat_id=subscriber.user_id, text=f"Today is {employee.name}'s birthday!")
    db.close()

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    job_queue = updater.job_queue
    job_queue.run_daily(notify_subscribers, time=datetime.time(hour=9, minute=0))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
