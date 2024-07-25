# Birthday Notification Service

## Описание
Сервис для поздравлений сотрудников с днем рождения с использованием FastAPI и Telegram бота.

## Установка и запуск

1. **Установите зависимости:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Инициализируйте базу данных:**
    ```sh
    python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
    ```

3. **Запустите FastAPI сервер:**
    ```sh
    uvicorn app:app --reload
    ```

4. **Настройте и запустите Telegram бота:**
    - В файле `telegram_bot.py` замените `your_telegram_bot_token` на токен вашего Telegram бота.
    - Запустите скрипт:
      ```sh
      python telegram_bot.py
      ```

## Использование

### Авторизация

- Получите токен, отправив POST запрос на `/token` с телом:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

### Получение списка сотрудников

- Отправьте GET запрос на `/employees`, добавив токен в заголовок Authorization.

### Добавление сотрудника

- Отправьте POST запрос на `/employees` с JSON телом:
    ```json
    {
        "name": "John Doe",
        "birthday": "1990-07-25"
    }
    ```

### Подписка на уведомления

- Отправьте POST запрос на `/subscribe` с JSON телом:
    ```json
    {
        "user_id": 1,
        "employee_id": 2
    }
    ```
    Добавьте токен в заголовок Authorization.

### Отписка от уведомлений

- Отправьте POST запрос на `/unsubscribe` с JSON телом:
    ```json
    {
        "user_id": 1,
        "employee_id": 2
    }
    ```
    Добавьте токен в заголовок Authorization.

### Взаимодействие с Telegram ботом

- Запустите Telegram бот и используйте команду `/start` для начала взаимодействия.

## Примечание
Обязательно замените `your_secret_key` и `your_telegram_bot_token` на ваши реальные значения.
