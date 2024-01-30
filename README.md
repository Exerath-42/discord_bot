# Discord Bot для получения информации по ссылке VK


## Команды
1. **$info**
   - Команда для получения общей информации о боте.

2. **$link [ссылка]**
   - Команда для получения дополнительной информации по указанной ссылке.

## Запуск
Для запуска бота, выполните следующие шаги:

1. Установите необходимые зависимости, выполнив команду:
   ```bash
   pip3 install discord.py requests python-dotenv beautifulsoup4
   ```

2. Создайте файл `.env` в рабочей директории проекта.

3. Добавьте следующие переменные в файл `.env`:
   - `bot_token`: Токен вашего Discord бота для доступа к API Discord.
   - `vk_service_access_key`: Ключ доступа к VK API для взаимодействия с сервисами VK.

   Пример содержимого файла `.env`:
   ```
   bot_token=YOUR_DISCORD_BOT_TOKEN
   vk_service_access_key=YOUR_VK_SERVICE_ACCESS_KEY
   ```

4. Запустите бота, используя команду:
   ```bash
   python3 bot.py
   ```

Бот теперь готов к использованию на вашем сервере Discord!