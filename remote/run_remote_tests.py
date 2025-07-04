#!/usr/bin/env python3
"""
Скрипт для запуска тестов на удаленном Mac
"""
import subprocess
import sys
import argparse
from remote_config import RemoteConfig


def run_remote_tests(
    remote_ip: str = None,
    test_file: str = None,
    service_type: str = "chrome",
    use_proxy: bool = False,
    verbose: bool = True
):
    """Запуск тестов на удаленном Mac"""
    
    # Используем IP из конфигурации или переданный
    if remote_ip:
        RemoteConfig.REMOTE_MAC_IP = remote_ip
    
    # Получаем URL удаленного браузера
    remote_url = RemoteConfig.get_remote_browser_url(service_type)
    
    # Формируем команду pytest
    cmd = [
        "python", "-m", "pytest",
        f"--remote-browser={remote_url}"
    ]
    
    # Добавляем файл тестов если указан
    if test_file:
        cmd.append(test_file)
    else:
        cmd.append("tests/")
    
    # Добавляем флаги
    if verbose:
        cmd.append("-v")
        cmd.append("-s")  # Показывать print statements
    
    # Добавляем маркеры для отчетности
    cmd.extend([
        "--tb=short",  # Короткий traceback
        "--durations=10"  # Показать 10 самых медленных тестов
    ])
    
    print(f"🚀 Запуск тестов на удаленном Mac: {RemoteConfig.REMOTE_MAC_IP}")
    print(f"📡 Remote URL: {remote_url}")
    print(f"🔧 Command: {' '.join(cmd)}")
    print("=" * 50)
    
    # Запускаем тесты
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️ Тестирование прервано пользователем")
        return 1
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        return 1


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="Запуск Playwright тестов на удаленном Mac")
    
    parser.add_argument(
        "--remote-ip",
        default=RemoteConfig.REMOTE_MAC_IP,
        help=f"IP адрес удаленного Mac (по умолчанию: {RemoteConfig.REMOTE_MAC_IP})"
    )
    
    parser.add_argument(
        "--test-file",
        help="Конкретный файл тестов для запуска (по умолчанию: все тесты)"
    )
    
    parser.add_argument(
        "--service-type",
        choices=["chrome", "selenium", "chromedriver"],
        default="chrome",
        help="Тип сервиса для подключения (по умолчанию: chrome)"
    )
    
    parser.add_argument(
        "--use-proxy",
        action="store_true",
        help="Использовать прокси настройки"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Тихий режим (без verbose вывода)"
    )
    
    args = parser.parse_args()
    
    # Запускаем тесты
    exit_code = run_remote_tests(
        remote_ip=args.remote_ip,
        test_file=args.test_file,
        service_type=args.service_type,
        use_proxy=args.use_proxy,
        verbose=not args.quiet
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 