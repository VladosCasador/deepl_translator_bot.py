import deepl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

# Настроим логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Установите ваши API-ключи
TELEGRAM_TOKEN = '7363757291:AAGV-GXmfOdARY-spMmskdg4uGrlVfVwaz8'
DEEPL_API_KEY = 'f5078d75-71b4-45e1-a591-37047254c35a:fx'

# Инициализация клиента DeepL
translator = deepl.Translator(DEEPL_API_KEY)

# Функция для перевода текста через DeepL API
def deepl_translate(text, target_language):
    try:
        # Переводим текст на целевой язык
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        logger.error(f"Ошибка при обращении к DeepL API: {e}")
        return "Ошибка при переводе через DeepL API. Попробуйте позже."

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Отправь мне текст, и я переведу его с русского на турецкий или с турецкого на русский."
    )

# Обработчик входящих сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text

    # Определяем язык сообщения: если текст содержит кириллицу, переводим на турецкий, если латиница — на русский
    if any('а' <= c <= 'я' or 'А' <= c <= 'Я' for c in user_message):
        # Перевод с русского на турецкий
        target_language = "TR"
    else:
        # Перевод с турецкого на русский
        target_language = "RU"

    translated_text = deepl_translate(user_message, target_language)
    await update.message.reply_text(translated_text)

# Основная функция для запуска бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
