#!/usr/bin/env python3
"""
CLI инструмент для управления тестовой конфигурацией
"""
import argparse
import subprocess
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(
        description="Менеджер конфигурации для Playwright тестов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Показать текущую конфигурацию
  python test_manager.py status

  # Переключиться на локальный режим
  python test_manager.py local

  # Переключиться на удаленный режим
  python test_manager.py remote

  # Обновить IP удаленного Mac
  python test_manager.py remote --ip 192.168.1.100

  # Включить прокси
  python test_manager.py proxy --enable

  # Запустить тесты
  python test_manager.py run
  python test_manager.py run --file tests/test_simple.py
  python test_manager.py run --smoke
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда status
    status_parser = subparsers.add_parser('status', help='Показать текущую конфигурацию')
    
    # Команда local
    local_parser = subparsers.add_parser('local', help='Переключиться на локальный режим')
    local_parser.add_argument('--headless', action='store_true', help='Запускать браузер в headless режиме')
    local_parser.add_argument('--slow-mo', type=int, default=100, help='Замедление в мс (по умолчанию: 100)')
    
    # Команда remote
    remote_parser = subparsers.add_parser('remote', help='Переключиться на удаленный режим')
    remote_parser.add_argument('--ip', help='IP адрес удаленного Mac')
    remote_parser.add_argument('--port', type=int, default=9222, help='Порт (по умолчанию: 9222)')
    remote_parser.add_argument('--service', choices=['chrome', 'selenium', 'chromedriver'], 
                              default='chrome', help='Тип сервиса')
    
    # Команда proxy
    proxy_parser = subparsers.add_parser('proxy', help='Управление прокси')
    proxy_group = proxy_parser.add_mutually_exclusive_group(required=True)
    proxy_group.add_argument('--enable', action='store_true', help='Включить прокси')
    proxy_group.add_argument('--disable', action='store_true', help='Отключить прокси')
    proxy_parser.add_argument('--host', help='Хост прокси')
    proxy_parser.add_argument('--port', type=int, help='Порт прокси')
    
    # Команда run
    run_parser = subparsers.add_parser('run', help='Запустить тесты')
    run_parser.add_argument('--file', help='Конкретный файл тестов')
    run_parser.add_argument('--smoke', action='store_true', help='Запустить только smoke тесты')
    run_parser.add_argument('--regression', action='store_true', help='Запустить regression тесты')
    run_parser.add_argument('--slow', action='store_true', help='Запустить slow тесты')
    run_parser.add_argument('--auth', action='store_true', help='Запустить auth тесты')
    run_parser.add_argument('--parallel', type=int, help='Количество параллельных процессов')
    run_parser.add_argument('--verbose', action='store_true', help='Подробный вывод')
    run_parser.add_argument('--quiet', action='store_true', help='Тихий режим')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        config = ConfigManager("config/test_config.json")
        
        if args.command == 'status':
            handle_status(config)
        elif args.command == 'local':
            handle_local(config, args)
        elif args.command == 'remote':
            handle_remote(config, args)
        elif args.command == 'proxy':
            handle_proxy(config, args)
        elif args.command == 'run':
            handle_run(config, args)
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


def handle_status(config: ConfigManager):
    """Обработка команды status"""
    config.print_current_config()


def handle_local(config: ConfigManager, args):
    """Обработка команды local"""
    config.set_test_mode('local')
    
    # Обновляем настройки если переданы
    if args.headless:
        config.config['local_settings']['headless'] = True
        print("🔧 Headless mode enabled")
    
    if args.slow_mo != 100:
        config.config['local_settings']['slow_mo'] = args.slow_mo
        print(f"🔧 Slow motion set to: {args.slow_mo}ms")
    
    config.save_config()
    config.print_current_config()


def handle_remote(config: ConfigManager, args):
    """Обработка команды remote"""
    config.set_test_mode('remote')
    
    # Обновляем настройки если переданы
    if args.ip:
        config.update_remote_ip(args.ip)
    
    if args.port != 9222:
        config.config['remote_settings']['port'] = args.port
        print(f"🔧 Remote port set to: {args.port}")
    
    if args.service != 'chrome':
        config.config['remote_settings']['service_type'] = args.service
        print(f"🔧 Service type set to: {args.service}")
    
    config.save_config()
    config.print_current_config()


def handle_proxy(config: ConfigManager, args):
    """Обработка команды proxy"""
    if args.enable:
        config.config['remote_settings']['use_proxy'] = True
        print("🔄 Proxy enabled")
    elif args.disable:
        config.config['remote_settings']['use_proxy'] = False
        print("🔄 Proxy disabled")
    
    # Обновляем настройки прокси если переданы
    if args.host:
        config.config['remote_settings']['proxy_host'] = args.host
        print(f"🌐 Proxy host set to: {args.host}")
    
    if args.port:
        config.config['remote_settings']['proxy_port'] = args.port
        print(f"🌐 Proxy port set to: {args.port}")
    
    config.save_config()
    config.print_current_config()


def handle_run(config: ConfigManager, args):
    """Обработка команды run"""
    cmd = ["python", "-m", "pytest"]
    
    # Добавляем файл тестов
    if args.file:
        cmd.append(args.file)
    else:
        cmd.append("tests/")
    
    # Добавляем маркеры
    markers = []
    if args.smoke:
        markers.append("smoke")
    if args.regression:
        markers.append("regression")
    if args.slow:
        markers.append("slow")
    if args.auth:
        markers.append("auth")
    
    if markers:
        cmd.extend(["-m", " or ".join(markers)])
    
    # Добавляем параллельность
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Добавляем вербозность
    if args.verbose:
        cmd.append("-v")
        cmd.append("-s")
    elif args.quiet:
        cmd.append("-q")
    else:
        cmd.append("-v")  # По умолчанию verbose
    
    # Добавляем дополнительные флаги
    cmd.extend([
        "--tb=short",
        "--durations=10"
    ])
    
    print(f"🚀 Запуск тестов в режиме: {config.get_test_mode()}")
    if config.is_remote_mode():
        print(f"📡 Remote URL: {config.get_remote_url()}")
    
    print(f"🔧 Command: {' '.join(cmd)}")
    print("=" * 50)
    
    # Запускаем тесты
    try:
        result = subprocess.run(cmd, cwd=".", check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️ Тестирование прервано пользователем")
        sys.exit(1)


if __name__ == "__main__":
    main() 