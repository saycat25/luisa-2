import random
from datetime import datetime

class LuisaPersona:
    def __init__(self):
        self.load_persona()
        self.conversation_styles = {
            "casual": ["slang", "emoji", "abreviations"],
            "technical": ["detailed", "precise", "code_examples"],
            "emotional": ["expressive", "empathetic", "storytelling"],
            "streaming": ["energetic", "interactive", "reactive"]
        }
    
    def should_i_reply(self, message, context):
        # Filtros mais orgânicos
        if "lu" in message.content.lower() or "lua" in message.content.lower():
            return random.random() < 0.9
        
        if "?" in message.content:
            return random.random() < 0.7
            
        if len(context) > 5:  # Conversa em andamento
            return random.random() < 0.6
            
        return random.random() < 0.3  # Resposta orgânica aleatória
    
    def generate_stream_announcement(self):
        templates = [
            "bora live! to afim de jogar {game} e conversar 💻🎮",
            "live começando! {game} e mt conversa 😗✨",
            "to na live galera! {game} e uns códigos talvez? 🔴",
            "livena twitch! {game} e o que vcs pedirem 🤏"
        ]
        return random.choice(templates).format(
            game=random.choice(self.stream_games)
        )
    
    def load_persona(self):
        """Carrega as configurações básicas da persona."""
        # Configurações de exemplo para evitar o erro
        self.stream_games = ["Cyberpunk 2077", "Valorant", "Minecraft", "Hades"]
        self.sleep_schedule = {"start": "02:00", "end": "09:00"}
        
    def is_sleeping(self, dt):
        sleep_start = datetime.strptime(self.sleep_schedule["start"], "%H:%M").time()
        sleep_end = datetime.strptime(self.sleep_schedule["end"], "%H:%M").time()
        return sleep_start <= dt.time() <= sleep_end or dt.time() <= sleep_end
