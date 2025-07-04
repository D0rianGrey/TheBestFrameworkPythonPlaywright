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

        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_config(self) -> None:
        """Сохранение конфигурации в файл"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        print(f"✅ Configuration saved to {self.config_file}")

    def get_test_mode(self) -> str:
        """Получить текущий режим тестирования"""
        # Приоритет: переменная окружения > конфигурация
        return os.getenv("TEST_MODE", self.config.get("test_mode", "local"))

    def set_test_mode(self, mode: str) -> None:
        """Установить режим тестирования"""
        if mode not in ["local", "remote"]:
            raise ValueError("Mode must be 'local' or 'remote'")

        self.config["test_mode"] = mode
        self.config["remote_settings"]["enabled"] = mode == "remote"
        print(f"🔧 Test mode set to: {mode}")

    def is_remote_mode(self) -> bool:
        """Проверить, включен ли удаленный режим"""
        return self.get_test_mode() == "remote"

    def get_remote_url(self) -> Optional[str]:
        """Получить URL удаленного браузера"""
        if not self.is_remote_mode():
            return None

        # Приоритет: переменные окружения > конфигурация
        ip = os.getenv("REMOTE_MAC_IP", self.config["remote_settings"].get("mac_ip"))
        port = os.getenv(
            "REMOTE_PORT", str(self.config["remote_settings"].get("port", 9222))
        )
        service_type = os.getenv(
            "SERVICE_TYPE", self.config["remote_settings"].get("service_type", "chrome")
        )

        # Если IP уже содержит протокол и порт, используем его как есть
        if ip and ("://" in ip or "/" in ip):
            # Добавляем протокол если его нет
            if not ip.startswith("ws://") and not ip.startswith("http://"):
                return f"ws://{ip}"
            return ip

        # Иначе формируем URL стандартным способом
        if service_type == "chrome":
            return f"ws://{ip}:{port}"
        elif service_type == "selenium":
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
            # Для локального режима - приоритет переменным окружения
            headless = (
                os.getenv(
                    "HEADLESS",
                    str(self.config["local_settings"].get("headless", False)),
                ).lower()
                == "true"
            )
            slow_mo = int(
                os.getenv(
                    "SLOW_MO", str(self.config["local_settings"].get("slow_mo", 100))
                )
            )

            return {"headless": headless, "slow_mo": slow_mo}

    def get_context_args(self) -> Dict[str, Any]:
        """Получить аргументы контекста браузера"""
        general = self.config["general_settings"]
        context_args = {
            "viewport": general.get("viewport", {"width": 1920, "height": 1080}),
            "ignore_https_errors": True,
        }

        return context_args

    def update_remote_ip(self, ip: str) -> None:
        """Обновить IP адрес удаленного Mac"""
        self.config["remote_settings"]["mac_ip"] = ip
        print(f"🌐 Remote Mac IP updated to: {ip}")

    def print_current_config(self) -> None:
        """Показать текущую конфигурацию"""
        mode = self.get_test_mode()
        print(f"\n📋 Current Configuration:")
        print(f"   Mode: {mode}")

        if mode == "remote":
            remote_url = self.get_remote_url()
            service_type = os.getenv(
                "SERVICE_TYPE",
                self.config["remote_settings"].get("service_type", "chrome"),
            )

            print(f"   Remote URL: {remote_url}")
            print(f"   Service Type: {service_type}")
        else:
            browser = os.getenv(
                "BROWSER", self.config["local_settings"].get("browser", "chromium")
            )
            headless = (
                os.getenv(
                    "HEADLESS",
                    str(self.config["local_settings"].get("headless", False)),
                ).lower()
                == "true"
            )
            print(f"   Browser: {browser}")
            print(f"   Headless: {headless}")

        print(f"   Viewport: {self.config['general_settings']['viewport']}")
        print()

    def print_env_vars(self) -> None:
        """Показать все связанные переменные окружения"""
        print("\n🌍 Environment Variables:")
        env_vars = [
            "TEST_MODE",
            "REMOTE_MAC_IP",
            "REMOTE_PORT",
            "SERVICE_TYPE",
            "BROWSER",
            "HEADLESS",
            "SLOW_MO",
        ]

        for var in env_vars:
            value = os.getenv(var)
            if value:
                print(f"   {var}: {value}")
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
    config.print_env_vars()

    # Переключение в удаленный режим
    config.set_test_mode("remote")
    config.print_current_config()

    # Переключение обратно в локальный режим
    config.set_test_mode("local")
    config.print_current_config()
