#!/usr/bin/env python3
"""
Простой тест для проверки удаленного подключения к Chrome через SSH туннель
"""
import asyncio
from playwright.async_api import async_playwright

async def test_remote_connection():
    """Тест удаленного подключения"""
    ws_url = "ws://localhost:9223/devtools/browser/5388b816-d0d0-430e-9f51-365f47c85264"
    
    print(f"🔗 Connecting to: {ws_url}")
    
    try:
        async with async_playwright() as p:
            # Подключаемся к удаленному браузеру
            browser = await p.chromium.connect_over_cdp(ws_url)
            print("✅ Successfully connected to remote browser!")
            
            # Получаем информацию о браузере
            contexts = browser.contexts
            print(f"📋 Browser contexts: {len(contexts)}")
            
            # Создаем новый контекст
            context = await browser.new_context()
            page = await context.new_page()
            
            # Переходим на тестовую страницу
            print("🌐 Navigating to the-internet.herokuapp.com...")
            await page.goto("https://the-internet.herokuapp.com/")
            
            # Получаем заголовок
            title = await page.title()
            print(f"📄 Page title: {title}")
            
            # Проверяем что заголовок правильный
            assert "The Internet" in title, f"Expected 'The Internet' in title, got: {title}"
            print("✅ Test passed! Remote testing is working!")
            
            # Закрываем
            await context.close()
            # Не закрываем browser - это удаленный браузер
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    result = asyncio.run(test_remote_connection())
    exit(0 if result else 1) 