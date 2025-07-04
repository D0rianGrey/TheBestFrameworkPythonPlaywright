# 🖥️ Настройка второго Mac для удаленного тестирования

## 🚀 Быстрая настройка (рекомендуемая)

### 1. Запустить Chrome с Remote Debugging

```bash
# На втором Mac выполни в терминале:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug \
  --no-first-run \
  --disable-default-apps \
  --disable-background-timer-throttling \
  --disable-backgrounding-occluded-windows \
  --disable-renderer-backgrounding
```

### 2. Проверить что работает

```bash
# На втором Mac:
curl http://localhost:9222/json/version

# Должен вернуть JSON с информацией о браузере
```

### 3. Узнать IP адрес

```bash
# На втором Mac:
ipconfig getifaddr en0
# Запомни этот IP (например: 192.168.195.104)
```

### 4. На первом Mac настроить подключение

```bash
# На первом Mac:
./test.sh remote 192.168.195.104
./test.sh run
```

## 🔧 Альтернативные способы

### Способ 2: Playwright браузер

Если нет Chrome или хочешь использовать Playwright браузер:

```bash
# На втором Mac установить Playwright:
pip install playwright
playwright install chromium

# Запустить браузер:
playwright open --browser=chromium --args="--remote-debugging-port=9222"
```

### Способ 3: Selenium Grid

Для более продвинутой настройки:

```bash
# На втором Mac скачать Selenium Server:
wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.15.0/selenium-server-4.15.0.jar

# Запустить Selenium Hub:
java -jar selenium-server-4.15.0.jar standalone --port 4444

# На первом Mac:
python test_manager.py remote --ip 192.168.195.104 --port 4444 --service selenium
```

## 🛠️ Удобные скрипты для второго Mac

### Создать скрипт для запуска Chrome

```bash
# На втором Mac создай файл start_chrome_debug.sh:
cat > ~/start_chrome_debug.sh << 'EOF'
#!/bin/bash
echo "🚀 Запуск Chrome с remote debugging на порту 9222..."

# Убиваем существующие процессы Chrome
pkill -f "Google Chrome" || true
sleep 2

# Запускаем Chrome с remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug-$(date +%s) \
  --no-first-run \
  --disable-default-apps \
  --disable-background-timer-throttling \
  --disable-backgrounding-occluded-windows \
  --disable-renderer-backgrounding \
  --window-size=1920,1080 \
  --window-position=0,0 &

echo "✅ Chrome запущен с remote debugging"
echo "📡 URL: ws://$(ipconfig getifaddr en0):9222"
echo "🔗 Проверить: curl http://localhost:9222/json/version"
EOF

# Сделать исполняемым:
chmod +x ~/start_chrome_debug.sh

# Запустить:
~/start_chrome_debug.sh
```

### Создать скрипт для проверки статуса

```bash
# На втором Mac создай файл check_debug_status.sh:
cat > ~/check_debug_status.sh << 'EOF'
#!/bin/bash
echo "🔍 Проверка статуса remote debugging..."

IP=$(ipconfig getifaddr en0)
echo "📡 IP адрес: $IP"

if curl -s http://localhost:9222/json/version > /dev/null; then
    echo "✅ Chrome remote debugging работает"
    echo "🌐 WebSocket URL: ws://$IP:9222"
    echo ""
    echo "📋 Информация о браузере:"
    curl -s http://localhost:9222/json/version | python3 -m json.tool
else
    echo "❌ Chrome remote debugging НЕ работает"
    echo "💡 Запустите: ~/start_chrome_debug.sh"
fi
EOF

chmod +x ~/check_debug_status.sh
```

## 🔍 Troubleshooting

### Проблема: Chrome не запускается

```bash
# Проверить что Chrome не запущен:
ps aux | grep Chrome

# Убить все процессы Chrome:
pkill -f "Google Chrome"

# Очистить временные файлы:
rm -rf /tmp/chrome-debug*

# Запустить заново
```

### Проблема: Порт 9222 занят

```bash
# Проверить что использует порт:
lsof -i :9222

# Убить процесс на порту:
sudo kill -9 $(lsof -t -i:9222)

# Или использовать другой порт:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9223 \
  # ... остальные параметры
```

### Проблема: Не могу подключиться с первого Mac

```bash
# На втором Mac проверить firewall:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Разрешить Chrome в firewall:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

# Проверить сетевое подключение с первого Mac:
# На первом Mac:
ping 192.168.195.104
telnet 192.168.195.104 9222
```

## 📱 Мониторинг

### Просмотр активных вкладок

```bash
# На втором Mac (или с первого):
curl http://192.168.195.104:9222/json
```

### Просмотр логов Chrome

```bash
# Запустить Chrome с логами:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --enable-logging \
  --log-level=0 \
  --user-data-dir=/tmp/chrome-debug \
  # ... остальные параметры
```

## 🎯 Автозапуск при старте Mac

### Создать LaunchAgent для автозапуска

```bash
# На втором Mac создать файл:
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.chrome.debug.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.chrome.debug</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Google Chrome.app/Contents/MacOS/Google Chrome</string>
        <string>--remote-debugging-port=9222</string>
        <string>--disable-web-security</string>
        <string>--user-data-dir=/tmp/chrome-debug</string>
        <string>--no-first-run</string>
        <string>--disable-default-apps</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Загрузить сервис:
launchctl load ~/Library/LaunchAgents/com.chrome.debug.plist

# Запустить сервис:
launchctl start com.chrome.debug
```

## 🏁 Итоговый чеклист

- [ ] Chrome запущен с `--remote-debugging-port=9222`
- [ ] Команда `curl http://localhost:9222/json/version` возвращает JSON
- [ ] IP адрес известен: `ipconfig getifaddr en0`
- [ ] Firewall настроен (если нужно)
- [ ] С первого Mac подключение работает: `telnet IP 9222`
- [ ] Тесты запускаются: `./test.sh remote IP && ./test.sh run` 