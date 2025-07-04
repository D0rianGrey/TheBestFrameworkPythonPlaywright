#!/usr/bin/env python3
"""
Скрипт для быстрого переключения между конфигурациями тестирования
Аналог настроек java.test.config в VS Code
"""
import os
import sys
import json
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager


class TestConfigSwitcher:
    """Переключатель конфигураций тестирования"""

    def __init__(self):
        self.config_manager = ConfigManager("config/test_config.json")
        self.vscode_settings_path = Path(".vscode/settings.json")

        # Предустановленные конфигурации
        self.configurations = {
            "local": {
                "description": "Local testing configuration",
                "env_vars": {
                    "TEST_MODE": "local",
                    "BROWSER": "chromium",
                    "HEADLESS": "false",
                },
            },
            "remote": {
                "description": "Remote testing configuration",
                "env_vars": {
                    "TEST_MODE": "remote",
                    "REMOTE_MAC_IP": "192.168.195.104",
                    "REMOTE_PORT": "9222",
                    "SERVICE_TYPE": "chrome",
                },
            },
            "remote-selenium": {
                "description": "Remote Selenium Grid configuration",
                "env_vars": {
                    "TEST_MODE": "remote",
                    "REMOTE_MAC_IP": "192.168.195.104",
                    "REMOTE_PORT": "4444",
                    "SERVICE_TYPE": "selenium",
                },
            },
            "headless": {
                "description": "Headless local testing",
                "env_vars": {"TEST_MODE": "local", "HEADLESS": "true"},
            },
        }

    def list_configurations(self):
        """Показать все доступные конфигурации"""
        print("\n🔧 Available Test Configurations:")
        print("=" * 50)

        for name, config in self.configurations.items():
            print(f"\n📋 {name}:")
            print(f"   Description: {config['description']}")
            print("   Environment Variables:")
            for key, value in config["env_vars"].items():
                print(f"     {key}: {value}")

    def apply_configuration(self, config_name: str):
        """Применить конфигурацию"""
        if config_name not in self.configurations:
            print(f"❌ Configuration '{config_name}' not found!")
            self.list_configurations()
            return False

        config = self.configurations[config_name]

        # Устанавливаем переменные окружения
        for key, value in config["env_vars"].items():
            os.environ[key] = value

        # Обновляем настройки VS Code
        self._update_vscode_settings(config_name, config)

        print(f"✅ Configuration '{config_name}' applied successfully!")
        print(f"   Description: {config['description']}")

        # Показываем текущую конфигурацию
        self.config_manager.print_current_config()

        return True

    def _update_vscode_settings(self, config_name: str, config: dict):
        """Обновить настройки VS Code"""
        if not self.vscode_settings_path.exists():
            print("⚠️  VS Code settings file not found, skipping update")
            return

        try:
            with open(self.vscode_settings_path, "r") as f:
                settings = json.load(f)

            # Обновляем переменные окружения для тестирования
            settings["python.testing.envVars"] = config["env_vars"]

            # Устанавливаем конфигурацию по умолчанию
            settings["python.testing.pytest.defaultConfiguration"] = (
                f"{config_name}-config"
            )

            with open(self.vscode_settings_path, "w") as f:
                json.dump(settings, f, indent=4)

            print(f"🔄 VS Code settings updated for '{config_name}' configuration")

        except Exception as e:
            print(f"⚠️  Failed to update VS Code settings: {e}")

    def get_current_config(self):
        """Получить текущую конфигурацию"""
        current_mode = self.config_manager.get_test_mode()

        # Определяем текущую конфигурацию по переменным окружения
        for name, config in self.configurations.items():
            if config["env_vars"].get("TEST_MODE") == current_mode:
                # Дополнительная проверка для удаленных конфигураций
                if current_mode == "remote":
                    current_service = os.getenv("SERVICE_TYPE", "chrome")
                    config_service = config["env_vars"].get("SERVICE_TYPE", "chrome")
                    if current_service != config_service:
                        continue

                return name, config

        return "custom", {"description": "Custom configuration", "env_vars": {}}

    def show_current_status(self):
        """Показать текущий статус"""
        current_name, current_config = self.get_current_config()

        print(f"\n📊 Current Status:")
        print(f"   Active Configuration: {current_name}")
        print(f"   Description: {current_config['description']}")

        self.config_manager.print_current_config()
        self.config_manager.print_env_vars()


def main():
    """Главная функция"""
    switcher = TestConfigSwitcher()

    if len(sys.argv) < 2:
        print("🚀 Test Configuration Switcher")
        print("Usage: python scripts/switch_config.py <command> [config_name]")
        print("\nCommands:")
        print("  list     - Show all available configurations")
        print("  apply    - Apply a specific configuration")
        print("  current  - Show current configuration status")
        print("\nExamples:")
        print("  python scripts/switch_config.py list")
        print("  python scripts/switch_config.py apply remote")
        print("  python scripts/switch_config.py current")
        return

    command = sys.argv[1].lower()

    if command == "list":
        switcher.list_configurations()

    elif command == "apply":
        if len(sys.argv) < 3:
            print("❌ Please specify configuration name")
            switcher.list_configurations()
            return

        config_name = sys.argv[2]
        switcher.apply_configuration(config_name)

    elif command == "current":
        switcher.show_current_status()

    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: list, apply, current")


if __name__ == "__main__":
    main()
