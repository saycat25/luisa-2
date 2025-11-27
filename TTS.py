import os
from gtts import gTTS
from io import BytesIO
import asyncio

class TextToSpeech:
    def __init__(self, lang='pt'):
        self.lang = lang
        self.audio_dir = "audio"
        os.makedirs(self.audio_dir, exist_ok=True)

    async def generate_speech(self, text, filename="speech.mp3"):
        """
        Gera um arquivo de áudio MP3 a partir do texto usando gTTS.
        Retorna o caminho completo do arquivo gerado.
        """
        filepath = os.path.join(self.audio_dir, filename)
        
        # gTTS é síncrono, então usamos asyncio.to_thread para não bloquear o loop de eventos
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._sync_generate, text, filepath)
        
        return filepath

    def _sync_generate(self, text, filepath):
        """Função síncrona para gerar o áudio."""
        try:
            tts = gTTS(text=text, lang=self.lang)
            tts.save(filepath)
            print(f"✅ Áudio gerado e salvo em: {filepath}")
        except Exception as e:
            print(f"❌ Erro ao gerar áudio com gTTS: {e}")
            raise

# Exemplo de uso:
# tts = TextToSpeech()
# audio_path = await tts.generate_speech("Olá, eu sou a Luísa Monteiro, sua assistente digital.", "intro.mp3")
