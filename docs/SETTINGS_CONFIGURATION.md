# Система настроек для удаленного тестирования

Аналог `java.test.config` из VS Code для Python + Playwright проекта.

## 🎯 Обзор

Система позволяет легко переключаться между различными конфигурациями тестирования:
- **Local** - локальное тестирование
- **Remote** - удаленное тестирование
- **Remote Selenium** - удаленное тестирование через Selenium Grid
- **Headless** - локальное тестирование без GUI

## 📁 Структура конфигурации

```
├── .vscode/settings.json          # VS Code настройки с предустановленными конфигурациями
├── config/
│   ├── config_manager.py          # Менеджер конфигурации
│   └── test_config.json           # Базовая конфигурация
├── scripts/
│   ├── switch_config.py           # Переключатель конфигураций
│   └── run_tests.sh               # Скрипт запуска тестов
```

## 🔧 VS Code настройки

В `.vscode/settings.json` определены предустановленные конфигурации:

```json
"python.testing.pytest.configurations": [
    {
        "name": "local-config",
        "description": "Local testing configuration",
        "envVars": {
            "TEST_MODE": "local",
            "BROWSER": "chromium",
            "HEADLESS": "false"
        }
    },
    {
        "name": "remote-config", 
        "description": "Remote testing configuration",
        "envVars": {
            "TEST_MODE": "remote",
            "REMOTE_MAC_IP": "192.168.195.104",
            "REMOTE_PORT": "9222",
            "SERVICE_TYPE": "chrome"
        }
    }
]
```

## 🚀 Способы использования

### 1. Через VS Code

1. Откройте Command Palette (`Cmd+Shift+P`)
2. Выберите `Python: Configure Tests`
3. Выберите нужную конфигурацию из списка
4. Запустите тесты через Test Explorer

### 2. Через скрипт переключения

```bash
# Показать все доступные конфигурации
python scripts/switch_config.py list

# Применить конфигурацию
python scripts/switch_config.py apply remote

# Показать текущий статус
python scripts/switch_config.py current
```

### 3. Через скрипт запуска тестов

```bash
# Локальные тесты
./scripts/run_tests.sh local

# Удаленные тесты
./scripts/run_tests.sh remote

# Удаленные тесты через Selenium Grid
./scripts/run_tests.sh remote-selenium

# Headless тесты
./scripts/run_tests.sh headless

# С дополнительными параметрами pytest
./scripts/run_tests.sh local -k test_simple -v
```

### 4. Через переменные окружения

```bash
# Установить переменные для удаленного тестирования
export TEST_MODE="remote"
export REMOTE_MAC_IP="192.168.195.104"
export REMOTE_PORT="9222"
export SERVICE_TYPE="chrome"

# Запустить тесты
python -m pytest tests/ -v
```

## 🌍 Переменные окружения

| Переменная | Описание | Значения по умолчанию |
|------------|----------|----------------------|
| `TEST_MODE` | Режим тестирования | `local` / `remote` |
| `REMOTE_MAC_IP` | IP удаленного Mac | `192.168.195.104` |
| `REMOTE_PORT` | Порт удаленного сервиса | `9222` (Chrome) / `4444` (Selenium) |
| `SERVICE_TYPE` | Тип удаленного сервиса | `chrome` / `selenium` |
| `BROWSER` | Браузер для локальных тестов | `chromium` / `firefox` / `webkit` |
| `HEADLESS` | Режим без GUI | `true` / `false` |
| `SLOW_MO` | Задержка между действиями (мс) | `100` |

## 📋 Доступные конфигурации

### Local Configuration
```json
{
    "TEST_MODE": "local",
    "BROWSER": "chromium", 
    "HEADLESS": "false"
}
```

### Remote Configuration
```json
{
    "TEST_MODE": "remote",
    "REMOTE_MAC_IP": "192.168.195.104",
    "REMOTE_PORT": "9222",
    "SERVICE_TYPE": "chrome"
}
```

### Remote Selenium Configuration
```json
{
    "TEST_MODE": "remote",
    "REMOTE_MAC_IP": "192.168.195.104", 
    "REMOTE_PORT": "4444",
    "SERVICE_TYPE": "selenium"
}
```

### Headless Configuration
```json
{
    "TEST_MODE": "local",
    "HEADLESS": "true"
}
```

## 🔍 Диагностика

### Проверка текущей конфигурации
```bash
python scripts/switch_config.py current
```

### Проверка переменных окружения
```bash
python -c "
import os
from config.config_manager import ConfigManager
config = ConfigManager('config/test_config.json')
config.print_env_vars()
"
```

### Проверка подключения к удаленному браузеру
```bash
# Для Chrome DevTools Protocol
curl -s http://192.168.195.104:9222/json/version

# Для Selenium Grid
curl -s http://192.168.195.104:4444/status
```

## 🛠️ Кастомизация

### Добавление новой конфигурации

1. Обновите `scripts/switch_config.py`:
```python
"my-custom": {
    "description": "My custom configuration",
    "env_vars": {
        "TEST_MODE": "local",
        "BROWSER": "firefox",
        "HEADLESS": "true"
    }
}
```

2. Обновите `.vscode/settings.json`:
```json
{
    "name": "my-custom-config",
    "description": "My custom configuration",
    "envVars": {
        "TEST_MODE": "local",
        "BROWSER": "firefox", 
        "HEADLESS": "true"
    }
}
```

3. Обновите `scripts/run_tests.sh`:
```bash
"my-custom")
    export TEST_MODE="local"
    export BROWSER="firefox"
    export HEADLESS="true"
    print_success "My custom configuration set"
    ;;
```

### Изменение IP адресов

Для быстрого изменения IP адресов без редактирования файлов:

```bash
# Через переменные окружения
export REMOTE_MAC_IP="192.168.1.100"

# Или через параметры конфигурации
python scripts/switch_config.py apply remote
```

## 🚨 Устранение неполадок

### Проблема: Тесты не подключаются к удаленному браузеру

**Решение:**
1. Проверьте доступность удаленного сервиса
2. Убедитесь в правильности IP адреса и порта
3. Проверьте, что на удаленной машине запущен Chrome с флагом `--remote-debugging-port=9222`

### Проблема: VS Code не видит конфигурации

**Решение:**
1. Перезапустите VS Code
2. Проверьте синтаксис `.vscode/settings.json`
3. Убедитесь, что Python extension установлен

### Проблема: Переменные окружения не применяются

**Решение:**
1. Проверьте активацию виртуального окружения
2. Убедитесь, что переменные установлены в правильной оболочке
3. Перезапустите терминал

## 📚 Примеры использования

### Быстрое переключение между конфигурациями

```bash
# Применить удаленную конфигурацию
python scripts/switch_config.py apply remote

# Запустить тесты
python -m pytest tests/ -v

# Переключиться обратно на локальную
python scripts/switch_config.py apply local
```

### Запуск конкретных тестов удаленно

```bash
# Запустить только тесты the-internet удаленно
./scripts/run_tests.sh remote -k test_the_internet

# Запустить с подробным выводом
./scripts/run_tests.sh remote -k test_simple -s -v
```

### Отладка конфигурации

```bash
# Показать текущую конфигурацию
python scripts/switch_config.py current

# Показать все доступные конфигурации
python scripts/switch_config.py list

# Проверить подключение к удаленному браузеру
curl -s http://192.168.195.104:9222/json/version
```

## 🔧 Настройка удаленного браузера

Для работы удаленного тестирования на Mac с IP `192.168.195.104` должен быть запущен Chrome с отладочным портом:

```bash
# На удаленном Mac
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --disable-web-security \
  --disable-features=VizDisplayCompositor
```

## 📝 Дополнительные ресурсы

- [REMOTE_TESTING_FINAL.md](./REMOTE_TESTING_FINAL.md) - Подробная настройка удаленного тестирования
- [QUICK_SETUP.md](./QUICK_SETUP.md) - Быстрая настройка проекта
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - Структура проекта 