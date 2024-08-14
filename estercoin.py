import logging
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Замените 'YOUR_API_TOKEN' на ваш токен API
API_TOKEN = '7491240904:AAFZWRRT8YQNJ7ZYun1NpBmx_bZmpcMJ1oI'

# Замените 'YOUR_WEBAPP_URL' на URL вашего веб-приложения
WEBAPP_URL = 'https://dimortix.github.io/EsterCoin/'

# Устанавливаем уровень логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения баланса пользователей
user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение и кнопку для открытия Web App."""
    user_id = update.effective_user.id
    balance = user_balances.get(user_id, 0)
    
    keyboard = [
        [KeyboardButton("Open EsterCoin Clicker", web_app=WebAppInfo(url=f"{WEBAPP_URL}?balance={balance}"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f'Welcome to EsterCoin Clicker! Your current balance: {balance} EsterCoins. Click the button below to start clicking:',
        reply_markup=reply_markup
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает данные, полученные от Web App."""
    data = update.effective_message.web_app_data.data
    user_id = update.effective_user.id
    
    try:
        balance = int(json.loads(data)['balance'])
        user_balances[user_id] = balance
        await update.message.reply_text(f"Your balance has been updated: {balance} EsterCoins")
    except (KeyError, ValueError, json.JSONDecodeError):
        await update.message.reply_text("Invalid data received from the Web App.")

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(API_TOKEN).build()
    
    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик данных от Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()