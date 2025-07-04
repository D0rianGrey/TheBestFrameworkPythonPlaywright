#!/usr/bin/env python3
"""
WebSocket прокси для Chrome Remote Debugging
Проксирует WebSocket подключения к Chrome на удаленном Mac
"""
import asyncio
import websockets
import json
import aiohttp
from urllib.parse import urlparse
import argparse


class ChromeProxy:
    def __init__(self, remote_host: str, remote_port: int = 9222, local_port: int = 9223):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port
        self.remote_base_url = f"http://{remote_host}:{remote_port}"
    
    async def proxy_websocket(self, websocket, path):
        """Проксирует WebSocket подключение к удаленному Chrome"""
        try:
            # Подключаемся к удаленному Chrome WebSocket
            remote_ws_url = f"ws://{self.remote_host}:{self.remote_port}{path}"
            print(f"Connecting to remote WebSocket: {remote_ws_url}")
            
            async with websockets.connect(remote_ws_url) as remote_ws:
                print(f"Connected to remote Chrome WebSocket")
                
                # Проксируем сообщения в обе стороны
                async def forward_to_remote():
                    async for message in websocket:
                        await remote_ws.send(message)
                
                async def forward_to_local():
                    async for message in remote_ws:
                        await websocket.send(message)
                
                # Запускаем проксирование в обе стороны
                await asyncio.gather(
                    forward_to_remote(),
                    forward_to_local()
                )
                
        except Exception as e:
            print(f"WebSocket proxy error: {e}")
    
    async def handle_http_request(self, request):
        """Обрабатывает HTTP запросы к Chrome DevTools API"""
        try:
            # Проксируем HTTP запрос к удаленному Chrome
            remote_url = f"{self.remote_base_url}{request.path_qs}"
            print(f"Proxying HTTP request: {remote_url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(remote_url) as response:
                    content = await response.text()
                    
                    # Заменяем localhost на наш прокси в WebSocket URL
                    if request.path.startswith('/json'):
                        content = content.replace(
                            f"ws://{self.remote_host}:{self.remote_port}",
                            f"ws://localhost:{self.local_port}"
                        )
                        content = content.replace(
                            f"ws://localhost:{self.remote_port}",
                            f"ws://localhost:{self.local_port}"
                        )
                    
                    return aiohttp.web.Response(
                        text=content,
                        status=response.status,
                        headers={'Content-Type': response.headers.get('Content-Type', 'application/json')}
                    )
        
        except Exception as e:
            print(f"HTTP proxy error: {e}")
            return aiohttp.web.Response(text=f"Proxy error: {e}", status=500)
    
    async def start_server(self):
        """Запускает прокси сервер"""
        print(f"Starting Chrome proxy server...")
        print(f"Remote Chrome: {self.remote_host}:{self.remote_port}")
        print(f"Local proxy: localhost:{self.local_port}")
        
        # HTTP сервер для DevTools API
        app = aiohttp.web.Application()
        app.router.add_get('/{path:.*}', self.handle_http_request)
        
        # Запускаем HTTP сервер
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, 'localhost', self.local_port)
        await site.start()
        
        # WebSocket сервер для DevTools Protocol
        ws_server = await websockets.serve(
            self.proxy_websocket,
            'localhost',
            self.local_port + 1  # WebSocket на порту +1
        )
        
        print(f"✅ Chrome proxy server started!")
        print(f"📡 HTTP API: http://localhost:{self.local_port}")
        print(f"🔌 WebSocket: ws://localhost:{self.local_port + 1}")
        print(f"🎯 Test: curl http://localhost:{self.local_port}/json/version")
        
        # Ждем завершения
        await asyncio.Future()  # run forever


async def main():
    parser = argparse.ArgumentParser(description='Chrome Remote Debugging Proxy')
    parser.add_argument('--remote-host', required=True, help='Remote Chrome host IP')
    parser.add_argument('--remote-port', type=int, default=9222, help='Remote Chrome port')
    parser.add_argument('--local-port', type=int, default=9223, help='Local proxy port')
    
    args = parser.parse_args()
    
    proxy = ChromeProxy(args.remote_host, args.remote_port, args.local_port)
    await proxy.start_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Proxy server stopped") 