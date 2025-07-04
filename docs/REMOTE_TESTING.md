# Удаленное тестирование на втором Mac

Этот документ описывает настройку и запуск Playwright тестов на удаленном Mac в локальной сети.

## Настройка второго Mac (сервер)

### 1. Установка Playwright
```bash
# Установка Python зависимостей
pip install playwright

# Установка браузеров
playwright install chromium
```

### 2. Запуск браузера в режиме отладки

#### Вариант A: Chrome/Chromium с remote debugging
```bash
# Запуск Chrome с remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug \
  --no-first-run \
  --disable-default-apps

# Или Chromium от Playwright
playwright open --browser=chromium --args="--remote-debugging-port=9222"
```

#### Вариант B: Selenium Grid (если нужен)
```bash
# Скачать Selenium Server
wget https://selenium-release.storage.googleapis.com/4.15/selenium-server-4.15.0.jar

# Запустить Selenium Hub
java -jar selenium-server-4.15.0.jar standalone --port 4444
```

#### Вариант C: ChromeDriver (если нужен)
```bash
# Скачать ChromeDriver
brew install chromedriver

# Запустить ChromeDriver
chromedriver --port=9515 --whitelisted-ips=192.168.0.0/16
```

### 3. Проверка доступности
```bash
# Проверить что сервис доступен
curl -I http://localhost:9222/json/version  # Chrome Debug
curl -I http://localhost:4444/status        # Selenium
curl -I http://localhost:9515/status        # ChromeDriver
```

## Настройка первого Mac (клиент)

### 1. Обновление конфигурации
Отредактируй файл `remote_config.py`:
```python
# Укажи IP адрес второго Mac
REMOTE_MAC_IP = "192.168.195.104"  # Замени на актуальный IP

# Настрой прокси если нужно
PROXY_HOST = "192.168.224.45"
PROXY_PORT = 3128
```

### 2. Запуск тестов

#### Простой запуск
```bash
# Запуск всех тестов на удаленном Mac
python run_remote_tests.py

# Запуск конкретного файла тестов
python run_remote_tests.py --test-file tests/test_simple.py

# Запуск с другим IP
python run_remote_tests.py --remote-ip 192.168.1.100
```

#### Ручной запуск через pytest
```bash
# Chrome Debug Protocol
python -m pytest tests/ --remote-browser=ws://192.168.195.104:9222 -v

# Selenium Grid
python -m pytest tests/ --remote-browser=http://192.168.195.104:4444 -v
```

#### Запуск с прокси
```bash
python run_remote_tests.py --use-proxy
```

## Способы подключения

### 1. Chrome Debug Protocol (рекомендуемый)
- **Порт:** 9222
- **URL:** `ws://IP:9222`
- **Преимущества:** Быстрый, нативная поддержка Playwright
- **Недостатки:** Только Chrome/Chromium

### 2. Selenium Grid
- **Порт:** 4444
- **URL:** `http://IP:4444`
- **Преимущества:** Поддержка разных браузеров
- **Недостатки:** Медленнее, дополнительная настройка

### 3. ChromeDriver
- **Порт:** 9515
- **URL:** `http://IP:9515`
- **Преимущества:** Простая настройка
- **Недостатки:** Только Chrome, устаревший подход

## Troubleshooting

### Проблема: Не могу подключиться к удаленному браузеру
```bash
# Проверь сетевую доступность
ping 192.168.195.104

# Проверь открытые порты
nmap -p 9222,4444,9515 192.168.195.104

# Проверь firewall на втором Mac
sudo pfctl -sr | grep 9222
```

### Проблема: Браузер не запускается
```bash
# Убей все процессы Chrome
pkill -f "chrome\|chromium"

# Очисти временные файлы
rm -rf /tmp/chrome-debug

# Запусти заново
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug
```

### Проблема: Прокси не работает
```bash
# Проверь прокси настройки
curl -x http://192.168.224.45:3128 http://example.com

# Проверь bypass правила
export no_proxy="192.168.*,172.17.*,localhost,127.0.0.1,*.local"
```

## Примеры использования

### Базовый smoke test
```bash
python run_remote_tests.py --test-file tests/test_simple.py
```

### Regression тесты
```bash
python -m pytest tests/ --remote-browser=ws://192.168.195.104:9222 -m regression -v
```

### Параллельное выполнение
```bash
# Установи pytest-xdist
pip install pytest-xdist

# Запуск в несколько потоков
python -m pytest tests/ --remote-browser=ws://192.168.195.104:9222 -n 4 -v
```

## Мониторинг и отладка

### Просмотр активных сессий
```bash
# Chrome Debug Protocol
curl http://192.168.195.104:9222/json | jq '.'

# Selenium Grid
curl http://192.168.195.104:4444/status | jq '.'
```

### Логирование
```bash
# Включить детальное логирование
export DEBUG=pw:*
python run_remote_tests.py --test-file tests/test_simple.py
```

## Автоматизация

### Скрипт для запуска сервера
Создай файл `start_remote_server.sh` на втором Mac:
```bash
#!/bin/bash
echo "🚀 Starting remote browser server..."

# Убиваем старые процессы
pkill -f "chrome\|chromium"

# Очищаем временные файлы
rm -rf /tmp/chrome-debug

# Запускаем Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug \
  --no-first-run \
  --disable-default-apps &

echo "✅ Remote browser server started on port 9222"
echo "📡 Access URL: ws://$(ipconfig getifaddr en0):9222"
```

### Интеграция с CI/CD
```yaml
# .github/workflows/remote-tests.yml
name: Remote Tests
on: [push, pull_request]

jobs:
  remote-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run remote tests
        run: |
          python run_remote_tests.py --remote-ip ${{ secrets.REMOTE_MAC_IP }}
``` 