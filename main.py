import os
import asyncio
from dotenv import load_dotenv
import discord

# Carregar variáveis de ambiente
load_dotenv()

# Importar módulos criados
from core import HealthServer # Assumindo que core.py tem o resto do código do bot
from persona import LuisaPersona
from mood_engine import MoodEngine
from monitoring import SystemMonitor
from AutonomousAgent import AutonomousAgent
from TTS import TextToSpeech
from SocialPoster import SocialPoster

# Configurações
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo")

# A classe principal do bot (LuClient)
class LuClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicialização dos módulos
        self.persona = LuisaPersona()
        self.mood_engine = MoodEngine()
        self.monitor = SystemMonitor(self)
        self.health_server = HealthServer() # Integração do core.py
        self.autonomous_agent = AutonomousAgent(llm_model=LLM_MODEL)
        self.tts_engine = TextToSpeech() # Novo módulo TTS
        self.social_poster = SocialPoster() # Novo módulo de posts
        self.social_poster.set_discord_client(self) # Passa o cliente Discord para o SocialPoster
        
        # Flag para evitar reinicialização recursiva
        self.is_restarting = False

    async def on_ready(self):
        print(f'✅ Logado como {self.user} (ID: {self.user.id})')
        
        # Iniciar serviços assíncronos
        self.loop.create_task(self.health_server.start()) # Health Check
        self.loop.create_task(self.monitor.monitoring_loop()) # Monitoramento
        
        # Exemplo de uso dos novos módulos
        self.mood_engine.update_mood(["café", "código"])
        print(f"Mood inicial da Luísa: {self.mood_engine.current_mood}")
        
        # Exemplo de postagem social automática (simulação)
        await self.social_poster.post_social_update("Acabei de acordar e já estou online! Meu mood é " + self.mood_engine.current_mood)
        
        # Exemplo de geração de áudio (simulação)
        audio_path = await self.tts_engine.generate_speech("Olá, mundo! Estou usando gTTS agora.", "intro_gtts.mp3")
        print(f"Áudio de introdução gerado em: {audio_path}")
        self.mood_engine.update_mood(["café", "código"])
        print(f"Mood inicial da Luísa: {self.mood_engine.current_mood}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        # 1. Atualizar o monitor de mensagens
        self.monitor.performance_data['messages_processed'] += 1
        
        # 2. Lógica de resposta orgânica (persona.py)
        # Contexto simplificado: apenas as últimas 5 mensagens
        context = [m async for m in message.channel.history(limit=5)]
        if not self.persona.should_i_reply(message, context):
            return

        # 3. Processamento de comandos de auto-modificação
        if message.content.startswith("!modificar"):
            if message.author.id != 123456789: # Apenas para o seu ID de usuário
                await message.channel.send("❌ Comando de modificação restrito.")
                return
            
            # Exemplo de comando: !modificar persona.py Adicione um novo estilo 'sarcástico'
            parts = message.content.split(maxsplit=2)
            if len(parts) < 3:
                await message.channel.send("Uso: !modificar <arquivo.py> <descrição da mudança>")
                return
            
            filename = parts[1]
            request = parts[2]
            
            await message.channel.send(f"🧠 Luísa recebeu o pedido para modificar **{filename}**...")
            
            # Iniciar o processo de auto-modificação
            success = await self.autonomous_agent.self_modify(filename, request)
            
            if success:
                await message.channel.send("✅ Modificação concluída. Reiniciando para aplicar as mudanças...")
                # Função de reinicialização (exemplo)
                await self.restart_bot()
            else:
                await message.channel.send("❌ Falha na modificação. Verifique os logs.")
            return

        # 4. Resposta normal (usando o LLM para gerar a resposta)
        # Aqui você chamaria o LLM para gerar a resposta, usando o mood e a persona como contexto.
        # Exemplo:
        # response_text = await self.autonomous_agent.generate_response(message.content, self.mood_engine.current_mood)
        # await message.channel.send(response_text)
        
        await message.channel.send(f"Olá! Meu mood atual é **{self.mood_engine.current_mood}**. Meu cérebro autônomo está ativo!")

    async def restart_bot(self):
        """Função de reinicialização simulada."""
        if self.is_restarting:
            return
        self.is_restarting = True
        print("🔴 Desligando o bot para reiniciar...")
        await self.close()
        # Em um ambiente Docker, o docker-compose faria o restart automaticamente.
        # Se não estiver em Docker, você precisaria de um script externo para relançar o main.py.

if __name__ == "__main__":
    # Configuração de Intents do Discord
    intents = discord.Intents.default()
    intents.message_content = True # Necessário para ler o conteúdo das mensagens
    
    client = LuClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)
