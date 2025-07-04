# 🎭 The Best Framework Python Playwright

Автоматизированный тестовый фреймворк на Python + Playwright для тестирования веб-приложений.

## 🚀 Быстрый старт с системой настроек

### Система конфигураций (аналог java.test.config)

Проект поддерживает быстрое переключение между различными режимами тестирования:

```bash
# Показать все доступные конфигурации
python scripts/switch_config.py list

# Переключиться на удаленное тестирование
python scripts/switch_config.py apply remote

# Запустить тесты локально
./scripts/run_tests.sh local

# Запустить тесты удаленно на IP 192.168.195.104
./scripts/run_tests.sh remote

# Запустить headless тесты
./scripts/run_tests.sh headless
```

### Доступные конфигурации:
- **local** - локальное тестирование
- **remote** - удаленное тестирование на 192.168.195.104:9222
- **remote-selenium** - удаленное тестирование через Selenium Grid на 192.168.195.104:4444  
- **headless** - локальное тестирование без GUI

### VS Code интеграция:
1. Откройте Command Palette (`Cmd+Shift+P`)
2. Выберите `Python: Configure Tests`
3. Выберите нужную конфигурацию из списка
4. Запустите тесты через Test Explorer

📚 **Подробная документация:** [docs/SETTINGS_CONFIGURATION.md](docs/SETTINGS_CONFIGURATION.md)

---

## 🚀 Особенности

- ✅ **Локальное и удаленное тестирование** - запуск тестов на втором Mac в сети
- ✅ **Простое переключение режимов** - одной командой
- ✅ **Фикстуры и хелперы** - готовые компоненты для быстрой разработки
- ✅ **Параметризованные тесты** - эффективное покрытие
- ✅ **Маркеры pytest** - группировка и фильтрация тестов
- ✅ **Подробная документация** - с примерами и best practices
- ✅ **Поддержка прокси** - для корпоративных сетей

## 📦 Установка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd TheBestFrameworkPythonPlaywright

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# или .venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Установить браузеры Playwright
playwright install chromium
```

## 🎯 Быстрый старт

### Локальное тестирование
```bash
# Простой способ
./test.sh local
./test.sh run

# Или через менеджер
python test_manager.py local
python test_manager.py run
```

### Удаленное тестирование
```bash
# Переключиться на удаленный режим
./test.sh remote 192.168.195.104

# Запустить тесты
./test.sh run
```

### Конкретные тесты
```bash
# Smoke тесты
./test.sh smoke

# Конкретный файл
./test.sh run tests/test_simple.py

# Через pytest напрямую
python -m pytest tests/test_simple.py -v
```

## 🔧 Управление конфигурацией

### Простые команды
```bash
# Показать статус
./test.sh status

# Переключение режимов
./test.sh local
./test.sh remote [IP]

# Запуск тестов
./test.sh run [файл]
./test.sh smoke
./test.sh regression
```

### Расширенные настройки
```bash
# Локальный режим с настройками
python test_manager.py local --headless --slow-mo 200

# Удаленный режим с настройками
python test_manager.py remote --ip 192.168.1.100 --port 9515 --service selenium

# Управление прокси
python test_manager.py proxy --enable --host 192.168.224.45 --port 3128
```

## 📁 Структура проекта

```
TheBestFrameworkPythonPlaywright/
├── tests/                          # Тесты
│   ├── conftest.py                 # Конфигурация pytest
│   ├── fixtures.py                 # Фикстуры и хелперы
│   ├── test_simple.py              # Простые тесты
│   ├── test_with_fixtures.py       # Тесты с фикстурами
│   ├── test_advanced_pytest.py     # Продвинутые примеры
│   └── test_the_internet.py        # Тесты для the-internet.herokuapp.com
├── docs/                           # Документация
│   ├── QUICK_SETUP.md             # Быстрая настройка
│   ├── REMOTE_TESTING.md          # Удаленное тестирование
│   └── README_TESTS.md            # Описание тестов
├── config_manager.py              # Менеджер конфигурации
├── test_manager.py                # CLI менеджер тестов
├── test.sh                        # Bash-скрипт для быстрого доступа
├── test_config.json               # Конфигурационный файл
├── requirements.txt               # Python зависимости
└── pytest.ini                    # Настройки pytest
```

## 🧪 Типы тестов

### По сложности
- **test_simple.py** - Базовые тесты для начинающих
- **test_with_fixtures.py** - Тесты с использованием фикстур
- **test_advanced_pytest.py** - Продвинутые возможности pytest
- **test_the_internet.py** - Реальные сценарии тестирования

### По маркерам
- **@pytest.mark.smoke** - Быстрые smoke тесты
- **@pytest.mark.regression** - Полные regression тесты
- **@pytest.mark.slow** - Медленные тесты
- **@pytest.mark.auth** - Тесты аутентификации

## 🌐 Удаленное тестирование

### Настройка второго Mac
```bash
# На втором Mac запустить Chrome с remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-debug
```

### Настройка первого Mac
```bash
# Узнать IP второго Mac
# На втором Mac: ipconfig getifaddr en0

# Переключиться на удаленный режим
./test.sh remote 192.168.195.104

# Запустить тесты
./test.sh run
```

## 📊 Запуск тестов

### Все тесты
```bash
python -m pytest tests/ -v
```

### По маркерам
```bash
python -m pytest tests/ -m smoke -v
python -m pytest tests/ -m "smoke or regression" -v
```

### Конкретные файлы
```bash
python -m pytest tests/test_simple.py -v
python -m pytest tests/test_simple.py::test_open_the_internet_website -v
```

### С параллельностью
```bash
python -m pytest tests/ -n 4 -v
```

## 🔍 Отладка

### Режим отладки
```bash
# Локально с видимым браузером
python test_manager.py local
python test_manager.py run --file tests/test_simple.py --verbose

# Один тест с подробным выводом
python -m pytest tests/test_simple.py::test_open_the_internet_website -v -s
```

### Логирование
```bash
# С подробным выводом
python -m pytest tests/ -v -s --tb=long

# С сохранением логов
python -m pytest tests/ -v --tb=short --durations=10
```

## 📚 Документация

- [Быстрая настройка](docs/QUICK_SETUP.md) - Пошаговое руководство
- [Удаленное тестирование](docs/REMOTE_TESTING.md) - Подробная настройка
- [Описание тестов](docs/README_TESTS.md) - Обзор всех тестов

## 🛠️ Troubleshooting

### Частые проблемы
1. **"Config file not found"** - Запустите `python config_manager.py`
2. **Не могу подключиться к удаленному Mac** - Проверьте IP и порт
3. **Тесты падают** - Проверьте конфигурацию `./test.sh status`

### Полезные команды
```bash
# Проверить статус
./test.sh status

# Переключиться на локальный режим
./test.sh local

# Отладить один тест
python -m pytest tests/test_simple.py::test_open_the_internet_website -v -s
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Коммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Пушьте в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для деталей.

## 🎯 Roadmap

- [ ] Интеграция с CI/CD (GitHub Actions)
- [ ] Поддержка Docker контейнеров
- [ ] Веб-интерфейс для управления тестами
- [ ] Интеграция с Allure отчетами
- [ ] Поддержка мобильного тестирования
