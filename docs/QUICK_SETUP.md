# Быстрая настройка локального и удаленного тестирования

## 🚀 Быстрый старт

### 1. Проверить текущую конфигурацию
```bash
python test_manager.py status
```

### 2. Переключиться на локальный режим
```bash
python test_manager.py local
```

### 3. Переключиться на удаленный режим
```bash
# Обновить IP и переключиться
python test_manager.py remote --ip 192.168.195.104

# Или просто переключиться с текущими настройками
python test_manager.py remote
```

### 4. Запустить тесты
```bash
# Запуск в текущем режиме
python test_manager.py run

# Конкретный файл
python test_manager.py run --file tests/test_simple.py

# Только smoke тесты
python test_manager.py run --smoke
```

## 📋 Все команды

### Управление режимами
```bash
# Статус
python test_manager.py status

# Локальный режим
python test_manager.py local
python test_manager.py local --headless           # С headless браузером
python test_manager.py local --slow-mo 200        # С замедлением 200мс

# Удаленный режим
python test_manager.py remote
python test_manager.py remote --ip 192.168.1.100  # Другой IP
python test_manager.py remote --port 9515         # Другой порт
python test_manager.py remote --service selenium  # Selenium Grid
```

### Управление прокси
```bash
# Включить прокси
python test_manager.py proxy --enable

# Отключить прокси
python test_manager.py proxy --disable

# Обновить настройки прокси
python test_manager.py proxy --enable --host 192.168.224.45 --port 3128
```

### Запуск тестов
```bash
# Все тесты
python test_manager.py run

# Конкретный файл
python test_manager.py run --file tests/test_simple.py

# По маркерам
python test_manager.py run --smoke
python test_manager.py run --regression
python test_manager.py run --auth

# С параллельностью
python test_manager.py run --parallel 4

# Тихий режим
python test_manager.py run --quiet
```

## 🔧 Настройка второго Mac

### На втором Mac:
```bash
# Запустить Chrome с remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug \
  --no-first-run \
  --disable-default-apps

# Проверить что работает
curl http://localhost:9222/json/version
```

### На первом Mac:
```bash
# Узнать IP второго Mac
# На втором Mac выполни: ipconfig getifaddr en0

# Обновить конфигурацию
python test_manager.py remote --ip <IP_ВТОРОГО_MAC>

# Запустить тесты
python test_manager.py run
```

## 🛠️ Альтернативные способы

### Через переменные окружения
```bash
# Локальный режим
export TEST_MODE=local
python -m pytest tests/ -v

# Удаленный режим
export TEST_MODE=remote
python -m pytest tests/ -v
```

### Через параметры pytest
```bash
# Прямое указание удаленного браузера
python -m pytest tests/ --remote-browser=ws://192.168.195.104:9222 -v

# Указание режима
python -m pytest tests/ --test-mode=remote -v
```

### Редактирование конфигурации вручную
Отредактируй файл `test_config.json`:
```json
{
    "test_mode": "remote",
    "remote_settings": {
        "enabled": true,
        "mac_ip": "192.168.195.104",
        "service_type": "chrome",
        "port": 9222,
        "use_proxy": false
    }
}
```

## 📊 Примеры использования

### Ежедневная разработка (локально)
```bash
python test_manager.py local
python test_manager.py run --smoke
```

### Тестирование на втором Mac
```bash
python test_manager.py remote
python test_manager.py run --regression
```

### CI/CD pipeline
```bash
python test_manager.py local --headless
python test_manager.py run --parallel 4
```

### Отладка конкретного теста
```bash
python test_manager.py local
python test_manager.py run --file tests/test_simple.py --verbose
```

## 🔍 Troubleshooting

### Проблема: "Config file not found"
```bash
# Создать конфигурацию по умолчанию
python config_manager.py
```

### Проблема: Не могу подключиться к удаленному Mac
```bash
# Проверить доступность
ping 192.168.195.104

# Проверить порт
telnet 192.168.195.104 9222

# Обновить IP
python test_manager.py remote --ip <НОВЫЙ_IP>
```

### Проблема: Тесты падают
```bash
# Проверить конфигурацию
python test_manager.py status

# Запустить один тест для отладки
python test_manager.py run --file tests/test_simple.py --verbose
``` 