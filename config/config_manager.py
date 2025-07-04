"""
Менеджер конфигурации для переключения между локальным и удаленным режимом тестирования
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Менеджер конфигурации тестов"""
    
    def __init__(self, config_file: str = "test_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self) -> None:
        """Сохранение конфигурации в файл"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        print(f"✅ Configuration saved to {self.config_file}")
    
    def get_test_mode(self) -> str:
        """Получить текущий режим тестирования"""
        # Приоритет: переменная окружения > конфигурация
        return os.getenv('TEST_MODE', self.config.get('test_mode', 'local'))
    
    def set_test_mode(self, mode: str) -> None:
        """Установить режим тестирования"""
        if mode not in ['local', 'remote']:
            raise ValueError("Mode must be 'local' or 'remote'")
        
        self.config['test_mode'] = mode
        self.config['remote_settings']['enabled'] = (mode == 'remote')
        print(f"🔧 Test mode set to: {mode}")
    
    def is_remote_mode(self) -> bool:
        """Проверить, включен ли удаленный режим"""
        return self.get_test_mode() == 'remote'
    
    def get_remote_url(self) -> Optional[str]:
        """Получить URL удаленного браузера"""
        if not self.is_remote_mode():
            return None
        
        settings = self.config['remote_settings']
        service_type = settings.get('service_type', 'chrome')
        ip = settings.get('mac_ip')
        port = settings.get('port', 9222)
        
        # Если IP уже содержит протокол и порт, используем его как есть
        if ip and ('://' in ip or '/' in ip):
            # Добавляем протокол если его нет
            if not ip.startswith('ws://') and not ip.startswith('http://'):
                return f"ws://{ip}"
            return ip
        
        # Иначе формируем URL стандартным способом
        if service_type == 'chrome':
            return f"ws://{ip}:{port}"
        elif service_type == 'selenium':
            return f"http://{ip}:{port}"
        else:
            return f"http://{ip}:{port}"
    
    def get_browser_launch_args(self) -> Dict[str, Any]:
        """Получить аргументы запуска браузера"""
        if self.is_remote_mode():
            # Для удаленного режима возвращаем пустой dict
            # Подключение к удаленному браузеру происходит через connect(), а не launch()
            return {}
        else:
            # Для локального режима
            local_settings = self.config['local_settings']
            return {
                "headless": local_settings.get('headless', False),
                "slow_mo": local_settings.get('slow_mo', 100)
            }
    
    def get_context_args(self) -> Dict[str, Any]:
        """Получить аргументы контекста браузера"""
        general = self.config['general_settings']
        context_args = {
            "viewport": general.get('viewport', {"width": 1920, "height": 1080}),
            "ignore_https_errors": True
        }
        
        # Добавляем прокси если включен в удаленном режиме
        if self.is_remote_mode():
            remote_settings = self.config['remote_settings']
            if remote_settings.get('use_proxy', False):
                proxy_host = remote_settings.get('proxy_host')
                proxy_port = remote_settings.get('proxy_port')
                if proxy_host and proxy_port:
                    context_args["proxy"] = {
                        "server": f"http://{proxy_host}:{proxy_port}",
                        "bypass": "192.168.*,172.17.*,localhost,127.0.0.1,*.local"
                    }
        
        return context_args
    
    def update_remote_ip(self, ip: str) -> None:
        """Обновить IP адрес удаленного Mac"""
        self.config['remote_settings']['mac_ip'] = ip
        print(f"🌐 Remote Mac IP updated to: {ip}")
    
    def toggle_proxy(self) -> None:
        """Переключить использование прокси"""
        current = self.config['remote_settings']['use_proxy']
        self.config['remote_settings']['use_proxy'] = not current
        status = "enabled" if not current else "disabled"
        print(f"🔄 Proxy {status}")
    
    def print_current_config(self) -> None:
        """Показать текущую конфигурацию"""
        mode = self.get_test_mode()
        print(f"\n📋 Current Configuration:")
        print(f"   Mode: {mode}")
        
        if mode == 'remote':
            remote_url = self.get_remote_url()
            proxy_enabled = self.config['remote_settings']['use_proxy']
            print(f"   Remote URL: {remote_url}")
            print(f"   Proxy: {'enabled' if proxy_enabled else 'disabled'}")
        else:
            local_settings = self.config['local_settings']
            print(f"   Browser: {local_settings.get('browser', 'chromium')}")
            print(f"   Headless: {local_settings.get('headless', False)}")
        
        print(f"   Viewport: {self.config['general_settings']['viewport']}")
        print()


# Глобальный экземпляр менеджера конфигурации
config_manager = ConfigManager("config/test_config.json")


def get_config() -> ConfigManager:
    """Получить глобальный экземпляр менеджера конфигурации"""
    return config_manager


if __name__ == "__main__":
    # Пример использования
    config = ConfigManager()
    config.print_current_config()
    
    # Переключение в удаленный режим
    config.set_test_mode('remote')
    config.print_current_config()
    
    # Переключение обратно в локальный режим
    config.set_test_mode('local')
    config.print_current_config() 