#!/usr/bin/env python3
"""
Скрипт для запуска тестов на удаленном Mac
"""
import subprocess
import sys
import argparse
from typing import Optional
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.remote_config import RemoteConfig


def run_remote_tests(
    remote_ip: Optional[str] = None,
    test_file: Optional[str] = None,
    service_type: str = "chrome",
    use_proxy: bool = False,
    verbose: bool = True,
) -> int:
    """Запуск тестов на удаленном Mac"""

    # Используем IP из конфигурации или переданный
    current_ip = remote_ip if remote_ip else RemoteConfig.REMOTE_MAC_IP

    # Получаем URL удаленного браузера с нужным IP
    def get_remote_url(ip: str, service_type: str) -> str:
        """Получить URL удаленного браузера с указанным IP"""
        if service_type == "chrome":
            return f"ws://{ip}:{RemoteConfig.CHROME_DEBUG_PORT}"
        elif service_type == "selenium":
            return f"http://{ip}:{RemoteConfig.SELENIUM_HUB_PORT}"
        elif service_type == "chromedriver":
            return f"http://{ip}:{RemoteConfig.CHROMEDRIVER_PORT}"
        else:
            raise ValueError(f"Unknown service type: {service_type}")

    remote_url = get_remote_url(current_ip, service_type)

    # Формируем команду pytest
    cmd = ["python", "-m", "pytest", f"--remote-browser={remote_url}"]

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
    cmd.extend(
        [
            "--tb=short",  # Короткий traceback
            "--durations=10",  # Показать 10 самых медленных тестов
        ]
    )

    print(f"🚀 Запуск тестов на удаленном Mac: {current_ip}")
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


def main() -> None:
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="Запуск Playwright тестов на удаленном Mac"
    )

    parser.add_argument(
        "--remote-ip",
        default=RemoteConfig.REMOTE_MAC_IP,
        help=f"IP адрес удаленного Mac (по умолчанию: {RemoteConfig.REMOTE_MAC_IP})",
    )

    parser.add_argument(
        "--test-file",
        help="Конкретный файл тестов для запуска (по умолчанию: все тесты)",
    )

    parser.add_argument(
        "--service-type",
        choices=["chrome", "selenium", "chromedriver"],
        default="chrome",
        help="Тип сервиса для подключения (по умолчанию: chrome)",
    )

    parser.add_argument(
        "--use-proxy", action="store_true", help="Использовать прокси настройки"
    )

    parser.add_argument(
        "--quiet", action="store_true", help="Тихий режим (без verbose вывода)"
    )

    args = parser.parse_args()

    # Запускаем тесты
    exit_code = run_remote_tests(
        remote_ip=args.remote_ip,
        test_file=args.test_file,
        service_type=args.service_type,
        use_proxy=args.use_proxy,
        verbose=not args.quiet,
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
