#!/bin/bash

# Простой скрипт для управления тестами
# Использование: ./test.sh [local|remote|run] [опции]

set -e

# Функция помощи
show_help() {
    echo "🎯 Менеджер тестов Playwright"
    echo ""
    echo "Использование:"
    echo "  ./test.sh local                    # Переключиться на локальный режим"
    echo "  ./test.sh remote [IP]              # Переключиться на удаленный режим"
    echo "  ./test.sh run [файл]               # Запустить тесты"
    echo "  ./test.sh smoke                    # Запустить smoke тесты"
    echo "  ./test.sh status                   # Показать статус"
    echo "  ./test.sh help                     # Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  ./test.sh local"
    echo "  ./test.sh remote 192.168.1.100"
    echo "  ./test.sh run tests/test_simple.py"
    echo "  ./test.sh smoke"
}

# Проверка аргументов
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    "local")
        echo "🏠 Переключение на локальный режим..."
        python tools/test_manager.py local
        ;;
    
    "remote")
        if [ -n "$2" ]; then
            echo "🌐 Переключение на удаленный режим с IP: $2"
            python tools/test_manager.py remote --ip "$2"
        else
            echo "🌐 Переключение на удаленный режим..."
            python tools/test_manager.py remote
        fi
        ;;
    
    "run")
        if [ -n "$2" ]; then
            echo "🚀 Запуск тестов: $2"
            python tools/test_manager.py run --file "$2"
        else
            echo "🚀 Запуск всех тестов..."
            python tools/test_manager.py run
        fi
        ;;
    
    "smoke")
        echo "💨 Запуск smoke тестов..."
        python tools/test_manager.py run --smoke
        ;;
    
    "regression")
        echo "🔄 Запуск regression тестов..."
        python tools/test_manager.py run --regression
        ;;
    
    "status")
        python tools/test_manager.py status
        ;;
    
    "help"|"-h"|"--help")
        show_help
        ;;
    
    *)
        echo "❌ Неизвестная команда: $1"
        echo "Используйте './test.sh help' для справки"
        exit 1
        ;;
esac 