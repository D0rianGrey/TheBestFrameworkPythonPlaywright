#!/bin/bash

# Скрипт для запуска тестов с разными конфигурациями
# Аналог java.test.config для Python + Playwright

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовков
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Функция для вывода успеха
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Функция для вывода ошибки
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Функция для вывода предупреждения
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Функция показа помощи
show_help() {
    echo "🚀 Test Runner with Configuration Support"
    echo ""
    echo "Usage: $0 [CONFIG] [OPTIONS]"
    echo ""
    echo "Available Configurations:"
    echo "  local           - Local testing (default)"
    echo "  remote          - Remote testing"
    echo "  remote-selenium - Remote Selenium Grid"
    echo "  headless        - Headless local testing"
    echo ""
    echo "Options:"
    echo "  -h, --help      - Show this help"
    echo "  -v, --verbose   - Verbose output"
    echo "  -k PATTERN      - Run tests matching pattern"
    echo "  --markers       - Show available pytest markers"
    echo ""
    echo "Examples:"
    echo "  $0 local                    # Run local tests"
    echo "  $0 remote                   # Run remote tests"
    echo "  $0 headless -k test_simple  # Run specific test headless"
    echo ""
}

# Функция для установки конфигурации
set_configuration() {
    local config_name=$1
    
    case $config_name in
        "local")
            export TEST_MODE="local"
            export BROWSER="chromium"
            export HEADLESS="false"
            print_success "Local configuration set"
            ;;
        "remote")
            export TEST_MODE="remote"
            export REMOTE_MAC_IP="192.168.195.104"
            export REMOTE_PORT="9222"
            export SERVICE_TYPE="chrome"
            print_success "Remote configuration set"
            ;;
        "remote-selenium")
            export TEST_MODE="remote"
            export REMOTE_MAC_IP="192.168.195.104"
            export REMOTE_PORT="4444"
            export SERVICE_TYPE="selenium"
            print_success "Remote Selenium Grid configuration set"
            ;;
        "headless")
            export TEST_MODE="local"
            export HEADLESS="true"
            print_success "Headless local configuration set"
            ;;
        *)
            print_error "Unknown configuration: $config_name"
            echo "Available configurations: local, remote, remote-selenium, headless"
            exit 1
            ;;
    esac
}

# Функция для показа текущей конфигурации
show_current_config() {
    print_header "Current Configuration"
    python3 -c "
import sys
sys.path.insert(0, '.')
from config.config_manager import ConfigManager
config = ConfigManager('config/test_config.json')
config.print_current_config()
config.print_env_vars()
"
}

# Функция для проверки зависимостей
check_dependencies() {
    print_header "Checking Dependencies"
    
    # Проверка Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed"
        exit 1
    fi
    
    # Проверка виртуального окружения
    if [[ -z "$VIRTUAL_ENV" && ! -d ".venv" ]]; then
        print_warning "Virtual environment not detected"
        print_warning "Consider activating virtual environment: source .venv/bin/activate"
    fi
    
    # Проверка pytest
    if ! python3 -c "import pytest" &> /dev/null; then
        print_error "pytest is not installed. Run: pip install -r requirements.txt"
        exit 1
    fi
    
    # Проверка playwright
    if ! python3 -c "import playwright" &> /dev/null; then
        print_error "playwright is not installed. Run: pip install -r requirements.txt"
        exit 1
    fi
    
    print_success "All dependencies are available"
}

# Функция для запуска тестов
run_tests() {
    local pytest_args=("$@")
    
    print_header "Running Tests"
    
    # Базовые аргументы pytest
    local base_args=(
        "tests/"
        "-v"
        "--tb=short"
        "--color=yes"
    )
    
    # Объединяем базовые аргументы с пользовательскими
    local final_args=("${base_args[@]}" "${pytest_args[@]}")
    
    echo "Command: python3 -m pytest ${final_args[*]}"
    echo ""
    
    # Запуск тестов
    if python3 -m pytest "${final_args[@]}"; then
        print_success "Tests completed successfully"
    else
        print_error "Tests failed"
        exit 1
    fi
}

# Основная логика
main() {
    local config_name="local"
    local pytest_args=()
    
    # Парсинг аргументов
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            --markers)
                python3 -m pytest --markers
                exit 0
                ;;
            local|remote|remote-selenium|headless)
                config_name=$1
                shift
                ;;
            *)
                # Все остальные аргументы передаем в pytest
                pytest_args+=("$1")
                shift
                ;;
        esac
    done
    
    # Проверка зависимостей
    check_dependencies
    
    # Установка конфигурации
    set_configuration "$config_name"
    
    # Показ текущей конфигурации
    show_current_config
    
    # Запуск тестов
    run_tests "${pytest_args[@]}"
}

# Запуск основной функции
main "$@" 