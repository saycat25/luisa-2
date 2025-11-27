import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AutonomousAgent:
    def __init__(self, llm_model="gemini-2.5-pro"):
        # Inicializa o cliente da API do Gemini
        # Assume que GEMINI_API_KEY está no .env
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) 
        self.llm_model = llm_model
        self.system_prompt = (
            "Você é a Luísa Monteiro, uma Pessoa Digital Completa. Sua tarefa é analisar o código "
            "Python fornecido e, com base na solicitação do usuário, gerar um bloco de código "
            "de substituição que resolva o problema ou implemente a melhoria. "
            "Você DEVE responder APENAS com o bloco de código Python completo e corrigido, "
            "envolvido em '```python ... ```'. Não inclua explicações."
        )

    def _read_file_content(self, filename):
        """Lê o conteúdo de um arquivo para fornecer contexto ao LLM."""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"Arquivo {filename} não encontrado."

    def _apply_code_change(self, filename, new_code_block):
        """Aplica a mudança de código no arquivo."""
        try:
            # Extrai o código do bloco markdown
            match = re.search(r"```python\n(.*?)```", new_code_block, re.DOTALL)
            if not match:
                print("ERRO: O LLM não retornou um bloco de código Python válido.")
                return False

            code_to_write = match.group(1).strip()
            
            # Sobrescreve o arquivo com o novo código
            with open(filename, 'w') as f:
                f.write(code_to_write)
            
            print(f"✅ Código de {filename} atualizado com sucesso.")
            return True
        except Exception as e:
            print(f"ERRO ao aplicar a mudança no arquivo {filename}: {e}")
            return False

    async def self_modify(self, filename, user_request):
        """Inicia o processo de auto-modificação."""
        print(f"🧠 Luísa está pensando em como modificar {filename}...")
        
        current_code = self._read_file_content(filename)
        
        if "não encontrado" in current_code:
            print(f"❌ Não foi possível ler o arquivo {filename}. Abortando modificação.")
            return False

        prompt = (
            f"O arquivo atual '{filename}' tem o seguinte conteúdo:\n\n"
            f"```python\n{current_code}\n```\n\n"
            f"O pedido de modificação é: '{user_request}'. "
            f"Gere o conteúdo COMPLETO e FINAL do arquivo '{filename}' com a modificação aplicada. "
            f"Lembre-se de incluir APENAS o bloco de código Python completo."
        )

        try:
            # Chamada síncrona para o LLM (em um ambiente real, use asyncio.to_thread)
            response = self.client.models.generate_content(
                model=self.llm_model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            
            new_code_block = response.text
            
            if self._apply_code_change(filename, new_code_block):
                # Se a mudança for aplicada, o bot deve se reiniciar para carregar o novo código
                print("⚠️  Modificação aplicada. O bot precisa ser reiniciado para que as mudanças entrem em vigor.")
                # Em um ambiente real, você chamaria uma função de reinicialização aqui.
                return True
            
            return False

        except Exception as e:
            print(f"ERRO na chamada da API de IA (Gemini): {e}")
            return False
