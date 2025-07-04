# TheBestFrameworkPythonPlaywright 🎭

Полнофункциональный фреймворк для автоматизации тестирования с Playwright и Python.

## 🚀 Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
python -m pytest tests/ --headed --browser=chromium -v

# Запуск конкретного файла тестов
python -m pytest tests/test_simple.py -v
```

## 📁 Структура проекта

```
TheBestFrameworkPythonPlaywright/
├── tests/                          # Все тесты и тестовая инфраструктура
│   ├── conftest.py                 # Конфигурация pytest
│   ├── fixtures.py                 # Переиспользуемые фикстуры
│   ├── test_simple.py              # Базовые тесты
│   ├── test_with_fixtures.py       # Демонстрация фикстур  
│   ├── test_advanced_pytest.py     # Продвинутые примеры
│   └── test_the_internet.py        # Оригинальные тесты
├── docs/                           # Документация
│   ├── README_TESTS.md             # Детальное описание тестов
│   └── FIXTURES_SEPARATION_SUMMARY.md # История разработки
├── memory-bank/                    # Контекст проекта
├── requirements.txt                # Зависимости Python
├── pytest.ini                     # Конфигурация pytest
└── mypy.ini                       # Конфигурация типизации
```

## ✨ Особенности

- **Отделенные фикстуры** - переиспользуемые компоненты
- **Помощники навигации** - упрощенная работа с сайтом
- **Элемент-чекеры** - автоматизированные проверки
- **Параметризованные тесты** - гибкое тестирование
- **Маркеры pytest** - группировка тестов

## 📚 Документация

- [Детальное описание тестов](docs/README_TESTS.md)
- [История разработки](docs/FIXTURES_SEPARATION_SUMMARY.md)

## 🧪 Типы тестов

- `test_simple.py` - Базовые примеры
- `test_with_fixtures.py` - Демонстрация фикстур (16 тестов)
- `test_advanced_pytest.py` - Продвинутые возможности pytest
- `test_the_internet.py` - Оригинальные тесты

Всего **22+ тестов** покрывают различные аспекты the-internet.herokuapp.com
