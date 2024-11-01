import telebot
from datetime import datetime, timedelta
import time
import threading

TOKEN = '7890744856:AAEcwZl1HzwlEwDhO4fd2HURpDJqbHGfquM'
bot = telebot.TeleBot(TOKEN)

# Расписание занятий с указанием дней недели и домашнего задания
# Формат: 'имя_ученика': [("день недели", "время занятия", "текст домашнего задания")]
schedule = {
    'ученик1': [('Понедельник', '10:00', 'Прочитать главу 5 и решить задачи 1-10'),
                ('Пятница', '16:48', 'Подготовить презентацию по теме')],
    'ученик2': [('Среда', '12:00', 'Сделать лабораторную работу №3')]
}

# Словарь для хранения chat_id учеников
student_ids = {}


# Функция для отправки напоминаний
def send_reminders():
    days_map = {
        'Понедельник': 0,
        'Вторник': 1,
        'Среда': 2,
        'Четверг': 3,
        'Пятница': 4,
        'Суббота': 5,
        'Воскресенье': 6
    }

    while True:
        now = datetime.now()
        current_day = now.weekday()  # Получаем номер текущего дня недели (0 для понедельника, 1 для вторника и т.д.)
        for student, lessons in schedule.items():
            for lesson_day, lesson_time, homework in lessons:
                # Проверяем, совпадает ли текущий день недели с днем занятия
                if days_map[lesson_day] == current_day:
                    lesson_datetime = datetime.strptime(lesson_time, '%H:%M').replace(
                        year=now.year, month=now.month, day=now.day
                    )

                    # Проверка на наличие chat_id ученика в словаре
                    if student in student_ids:
                        # Напоминание за день до занятия (в тот же день накануне занятия)
                        if lesson_datetime - timedelta(days=1) <= now < lesson_datetime - timedelta(days=1) + timedelta(
                                minutes=1):
                            bot.send_message(
                                student_ids[student],
                                f"Напоминание: У вас завтра занятие в {lesson_time}!\nДомашнее задание: {homework}"
                            )
                            print(f"Отправлено напоминание за день для {student}")

                        # Напоминание за час до занятия
                        if lesson_datetime - timedelta(hours=1) <= now < lesson_datetime - timedelta(
                                hours=1) + timedelta(minutes=1):
                            bot.send_message(
                                student_ids[student],
                                f"Напоминание: У вас занятие через час в {lesson_time}!\nДомашнее задание: {homework}"
                            )
                            print(f"Отправлено напоминание за час для {student}")

        time.sleep(60)


# Запуск функции напоминаний в отдельном потоке
threading.Thread(target=send_reminders).start()


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который будет напоминать тебе о занятиях и домашнем задании.")


# Команда для сохранения chat_id с указанием имени ученика
@bot.message_handler(commands=['set_id'])
def set_id(message):
    try:
        # Извлекаем имя ученика из сообщения
        student_name = message.text.split()[1]
        student_ids[student_name] = message.chat.id
        bot.send_message(message.chat.id, f"Ваш chat_id сохранен под именем {student_name}!")
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите имя после команды /set_id.")


# Запуск бота
bot.polling()



