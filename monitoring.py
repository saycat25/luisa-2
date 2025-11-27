import psutil
import asyncio
from datetime import datetime

class SystemMonitor:
    def __init__(self, client):
        self.client = client
        self.performance_data = {
            "start_time": datetime.now(),
            "messages_processed": 0,
            "voice_sessions": 0,
            "streams_started": 0
        }
    
    async def monitoring_loop(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            # Monitorar recursos
            cpu_percent = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            
            # Alertas de performance
            if cpu_percent > 80:
                print(f"⚠️  CPU alta: {cpu_percent}%")
            if memory_usage > 85:
                print(f"⚠️  Memória alta: {memory_usage}%")
            
            # Log de status a cada 30 minutos
            if datetime.now().minute % 30 == 0:
                self.log_system_status()
            
            await asyncio.sleep(300)  # 5 minutos
    
    def log_system_status(self):
        status = f"""
📊 STATUS DO SISTEMA - {datetime.now()}
• Uptime: {datetime.now() - self.performance_data['start_time']}
• Mensagens processadas: {self.performance_data['messages_processed']}
• Sessões de voz: {self.performance_data['voice_sessions']}
• Lives realizadas: {self.performance_data['streams_started']}
• CPU: {psutil.cpu_percent()}%
• Memória: {psutil.virtual_memory().percent}%
        """
        print(status)
