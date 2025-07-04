"""
Конфигурация для удаленного тестирования на втором Mac
"""
import os
from typing import Dict, Any


class RemoteConfig:
    """Конфигурация для удаленного тестирования"""
    
    # IP адрес второго Mac
    REMOTE_MAC_IP = "192.168.195.104"
    
    # Порты для разных сервисов
    CHROME_DEBUG_PORT = 9222
    SELENIUM_HUB_PORT = 4444
    CHROMEDRIVER_PORT = 9515
    
    # Прокси настройки (если нужны)
    PROXY_HOST = "192.168.224.45"
    PROXY_PORT = 3128
    
    @classmethod
    def get_remote_browser_url(cls, service_type: str = "chrome") -> str:
        """Получить URL удаленного браузера"""
        if service_type == "chrome":
            return f"ws://{cls.REMOTE_MAC_IP}:{cls.CHROME_DEBUG_PORT}"
        elif service_type == "selenium":
            return f"http://{cls.REMOTE_MAC_IP}:{cls.SELENIUM_HUB_PORT}"
        elif service_type == "chromedriver":
            return f"http://{cls.REMOTE_MAC_IP}:{cls.CHROMEDRIVER_PORT}"
        else:
            raise ValueError(f"Unknown service type: {service_type}")
    
    @classmethod
    def get_proxy_config(cls) -> Dict[str, Any]:
        """Получить конфигурацию прокси"""
        return {
            "server": f"http://{cls.PROXY_HOST}:{cls.PROXY_PORT}",
            "bypass": "192.168.*,172.17.*,localhost,127.0.0.1,*.local"
        }
    
    @classmethod
    def get_browser_launch_args(cls, use_proxy: bool = False) -> Dict[str, Any]:
        """Получить аргументы запуска браузера"""
        args = {
            "headless": False,
            "slow_mo": 100,
            "ignore_https_errors": True
        }
        
        if use_proxy:
            proxy_config = cls.get_proxy_config()
            args["proxy"] = proxy_config
            
        return args


# Переменные окружения для удобства
def setup_remote_environment():
    """Настройка переменных окружения для удаленного тестирования"""
    os.environ["REMOTE_MAC_IP"] = RemoteConfig.REMOTE_MAC_IP
    os.environ["CHROME_DEBUG_URL"] = RemoteConfig.get_remote_browser_url("chrome")
    os.environ["SELENIUM_HUB_URL"] = RemoteConfig.get_remote_browser_url("selenium")


if __name__ == "__main__":
    # Пример использования
    config = RemoteConfig()
    print("Chrome Debug URL:", config.get_remote_browser_url("chrome"))
    print("Selenium Hub URL:", config.get_remote_browser_url("selenium"))
    print("Proxy Config:", config.get_proxy_config()) 