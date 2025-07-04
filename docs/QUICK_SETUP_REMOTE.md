# Быстрая настройка удаленного тестирования

## 🎯 Цель
Настроить систему для удаленного запуска тестов на Mac с IP `192.168.195.104` без использования прокси.

## ⚡ Быстрый старт

### 1. Проверка доступных конфигураций
```bash
python scripts/switch_config.py list
```

### 2. Переключение на удаленное тестирование
```bash
# Через скрипт переключения
python scripts/switch_config.py apply remote

# Или через скрипт запуска
./scripts/run_tests.sh remote
```

### 3. Запуск конкретных тестов
```bash
# Запустить только простые тесты удаленно
./scripts/run_tests.sh remote -k test_simple

# Запустить все тесты the-internet удаленно
./scripts/run_tests.sh remote -k test_the_internet
```

## 🔧 Настройка удаленного Mac (192.168.195.104)

На удаленном Mac должен быть запущен Chrome с отладочным портом:

```bash
# Запуск Chrome с удаленной отладкой
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --disable-web-security \
  --disable-features=VizDisplayCompositor
```

## 📋 Доступные конфигурации

| Конфигурация | Описание | IP | Порт | Тип |
|-------------|----------|----|----- |-----|
| `local` | Локальное тестирование | - | - | Chromium |
| `remote` | Удаленное тестирование | 192.168.195.104 | 9222 | Chrome |
| `remote-selenium` | Selenium Grid | 192.168.195.104 | 4444 | Selenium |
| `headless` | Локально без GUI | - | - | Headless |

## 🌍 Переменные окружения

Система автоматически устанавливает следующие переменные:

### Для remote конфигурации:
```bash
TEST_MODE=remote
REMOTE_MAC_IP=192.168.195.104
REMOTE_PORT=9222
SERVICE_TYPE=chrome
```

### Для local конфигурации:
```bash
TEST_MODE=local
BROWSER=chromium
HEADLESS=false
```

## 🔍 Диагностика

### Проверка текущей конфигурации
```bash
python scripts/switch_config.py current
```

### Проверка подключения к удаленному браузеру
```bash
# Проверка доступности Chrome DevTools
curl -s http://192.168.195.104:9222/json/version

# Ожидаемый ответ должен содержать информацию о браузере
```

### Проверка переменных окружения
```bash
# В PowerShell
echo $env:TEST_MODE
echo $env:REMOTE_MAC_IP

# В bash/zsh
echo $TEST_MODE
echo $REMOTE_MAC_IP
```

## 🚨 Устранение неполадок

### Проблема: Тесты не подключаются к удаленному браузеру

**Проверки:**
1. Удаленный Mac доступен: `ping 192.168.195.104`
2. Chrome запущен с правильными флагами
3. Порт 9222 открыт: `curl -s http://192.168.195.104:9222/json/version`

**Решения:**
- Перезапустить Chrome на удаленном Mac
- Проверить настройки файрвола
- Убедиться, что IP адрес правильный

### Проблема: VS Code не видит конфигурации

**Решения:**
1. Перезапустить VS Code
2. Проверить файл `.vscode/settings.json`
3. Установить Python extension

## 📚 Примеры использования

### Быстрое переключение
```bash
# Локальные тесты
python scripts/switch_config.py apply local
python -m pytest tests/ -v

# Удаленные тесты  
python scripts/switch_config.py apply remote
python -m pytest tests/ -v
```

### Запуск через скрипт
```bash
# Все тесты локально
./scripts/run_tests.sh local

# Только простые тесты удаленно
./scripts/run_tests.sh remote -k test_simple

# Headless режим
./scripts/run_tests.sh headless
```

### Прямое использование переменных окружения
```bash
# PowerShell
$env:TEST_MODE = "remote"
$env:REMOTE_MAC_IP = "192.168.195.104"
python -m pytest tests/test_simple.py -v

# Bash/Zsh
export TEST_MODE="remote"
export REMOTE_MAC_IP="192.168.195.104"
python -m pytest tests/test_simple.py -v
```

## ✅ Проверка работоспособности

```bash
# 1. Проверить конфигурации
python scripts/switch_config.py list

# 2. Применить удаленную конфигурацию
python scripts/switch_config.py apply remote

# 3. Проверить статус
python scripts/switch_config.py current

# 4. Запустить простой тест
./scripts/run_tests.sh remote -k test_simple
```

Если все шаги выполнены успешно, система готова к работе! 🎉 