# Adicionar ao final do core.py
from aiohttp import web
import threading

class HealthServer:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_get('/health', self.health_check)
        self.runner = None
        
    async def health_check(self, request):
        return web.json_response({
            "status": "healthy",
            "persona": "Luísa Monteiro",
            "uptime": "online",
            "memory_usage": "normal"
        })
    
    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '0.0.0.0', 8000)
        await site.start()
        print("✅ Health server running on port 8000")

# Adicionar no __init__ do LuClient:
# self.health_server = HealthServer()

# Adicionar no on_ready:
# self.loop.create_task(self.health_server.start())
