import random
from datetime import datetime, timedelta

class MoodEngine:
    def __init__(self):
        self.current_mood = "neutral"
        self.mood_intensity = 0.5
        self.mood_triggers = {
            "positive": ["café", "código", "live", "amigos", "musica"],
            "negative": ["bug", "fome", "sono", "erro", "delay"]
        }
        self.last_mood_change = datetime.now()
    
    def update_mood(self, events):
        for event in events:
            if any(trigger in event.lower() for trigger in self.mood_triggers["positive"]):
                self.mood_intensity += 0.1
            elif any(trigger in event.lower() for trigger in self.mood_triggers["negative"]):
                self.mood_intensity -= 0.15
        
        # Decaimento natural do humor
        time_diff = (datetime.now() - self.last_mood_change).seconds / 3600
        self.mood_intensity -= time_diff * 0.05
        
        # Limitar entre 0 e 1
        self.mood_intensity = max(0, min(1, self.mood_intensity))
        
        # Definir mood baseado na intensidade
        if self.mood_intensity > 0.7:
            self.current_mood = "happy"
        elif self.mood_intensity > 0.4:
            self.current_mood = "neutral"
        elif self.mood_intensity > 0.2:
            self.current_mood = "tired"
        else:
            self.current_mood = "frustrated"
        
        self.last_mood_change = datetime.now()
