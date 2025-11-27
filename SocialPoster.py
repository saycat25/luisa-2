import os
from dotenv import load_dotenv
from mastodon import Mastodon
import discord
import asyncio

load_dotenv()

class SocialPoster:
    def __init__(self):
        # Configurações do Mastodon
        self.mastodon_api_base_url = os.getenv("MASTODON_API_BASE_URL")
        self.mastodon_access_token = os.getenv("MASTODON_ACCESS_TOKEN")
        
        # Configurações do Discord (usaremos o cliente do bot para postar)
        self.discord_client = None
        self.discord_channel_id = os.getenv("DISCORD_POST_CHANNEL_ID")

        # Inicializa o cliente Mastodon
        if self.mastodon_api_base_url and self.mastodon_access_token:
            try:
                self.mastodon = Mastodon(
                    access_token=self.mastodon_access_token,
                    api_base_url=self.mastodon_api_base_url
                )
                print("✅ Cliente Mastodon inicializado.")
            except Exception as e:
                print(f"❌ Erro ao inicializar Mastodon: {e}")
                self.mastodon = None
        else:
            self.mastodon = None
            print("⚠️  Variáveis do Mastodon não configuradas.")

    def set_discord_client(self, client):
        """Define o cliente Discord para uso em posts."""
        self.discord_client = client

    async def post_to_mastodon(self, status_text):
        """Posta uma mensagem no Mastodon."""
        if not self.mastodon:
            print("❌ Mastodon não configurado. Postagem ignorada.")
            return False
        
        try:
            # A chamada à API do Mastodon é síncrona, rodamos em um executor
            loop = asyncio.get_event_loop()
            toot = await loop.run_in_executor(None, self.mastodon.status_post, status_text)
            print(f"✅ Postagem no Mastodon bem-sucedida: {toot.url}")
            return True
        except Exception as e:
            print(f"❌ Erro ao postar no Mastodon: {e}")
            return False

    async def post_to_discord(self, message_text):
        """Posta uma mensagem em um canal específico do Discord."""
        if not self.discord_client or not self.discord_channel_id:
            print("❌ Cliente Discord ou ID do canal não configurados. Postagem ignorada.")
            return False
        
        try:
            channel = self.discord_client.get_channel(int(self.discord_channel_id))
            if channel:
                await channel.send(message_text)
                print(f"✅ Postagem no Discord bem-sucedida no canal {channel.name}.")
                return True
            else:
                print(f"❌ Canal Discord com ID {self.discord_channel_id} não encontrado.")
                return False
        except Exception as e:
            print(f"❌ Erro ao postar no Discord: {e}")
            return False

    async def post_social_update(self, text):
        """Posta a mesma mensagem em ambas as plataformas."""
        mastodon_success = await self.post_to_mastodon(text)
        discord_success = await self.post_to_discord(text)
        return mastodon_success or discord_success

# Exemplo de uso (será chamado do main.py)
# poster = SocialPoster()
# await poster.post_social_update("Estou online agora! Venham conversar.")
