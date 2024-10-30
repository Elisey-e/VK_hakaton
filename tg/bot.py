import logging
import threading
import time
from queue import Queue
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
print("Starting loading model")
import qwen_tg_pipe
print("Ended loading model")

idx = 0

# Логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Очередь для сообщений
message_queue = Queue()

# Флаг, который сигнализирует о занятости бота
bot_busy = False

# Функция, которая будет применяться к сообщениям (пример: перевод текста в верхний регистр)
def process_message(update: Update, text: str) -> str:
    global idx
    print(f"Caught new message id {idx}")
    print(text)
    update.message.reply_text("Увидел ваше сообщение, пожалуйста, дождитесь ответа, я не быстрый)))")
    res = qwen_tg_pipe.generate_answer(text)
    print(f"Ended analyzing message id {idx}")
    idx += 1
    return res


# Функция для старта, которая срабатывает на команду /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне любое сообщение, и я преобразую его. Генерирую ответ на запрос около 20 секунд. Если не отвечаю, что принял запрос, значит выключен(либо отвечаю другому человеку), СПАМИТЬ НАДО пока не отвечу что все ок.')

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    global bot_busy
    
    # Если бот занят, говорим пользователю подождать и показываем количество сообщений в очереди
    if bot_busy:
        position_in_queue = message_queue.qsize() + 1  # Сколько сообщений перед пользователем
        update.message.reply_text(f"Бот занят, жди своей очереди. Сообщений перед тобой: {position_in_queue}")
    message_queue.put((update, context))


def message_worker():
    global bot_busy
    
    while True:
        if not message_queue.empty():
            bot_busy = True
            update, context = message_queue.get()  # Получаем сообщение из очереди
            
            user_message = update.message.text
            try:
                result = process_message(update, user_message)  # Долгая обработка
                update.message.reply_text(result)  # Отправляем результат пользователю
                message_queue.task_done()  # Сообщаем, что задача выполнена
            except:
                try:
                    update.message.reply_text("Ошибка, введи запрос снова. Повторяю: СПАМЬ В МЕНЯ ПОЖАЛУЙСТА, СПАМЬ МНОГО, твои сообщения иногда просто испаряются.")
                except:
                    pass
                print("Ошибка, введи запрос снова")
        else:
            bot_busy = False

# Функция для обработки ошибок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} вызвало ошибку {context.error}')
    update.message.reply_text("Произошла ошибка, напишите снова")
    update.message.reply_text(f'Update {update} вызвало ошибку {context.error}')

def main() -> None:
    # Ваш токен от BotFather
    TOKEN = '7656025485:AAHgt5BB8Yk5UIaD3QAvcuI0seN0mI3v9-g'

    # Создаем апдейтер и диспетчер
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))  # Обработка команды /start
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  # Обработка текстовых сообщений
    dispatcher.add_error_handler(error)  # Обработка ошибок

    # Запускаем поток для обработки очереди сообщений
    threading.Thread(target=message_worker, daemon=True).start()

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    
    main()
