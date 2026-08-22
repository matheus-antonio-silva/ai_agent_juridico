from json import load
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model = 'openai/gpt-4o-mini'
)

resposta = llm.call(
    'Explique em uma frase o que é Direito do consumidor'
)

print(resposta)