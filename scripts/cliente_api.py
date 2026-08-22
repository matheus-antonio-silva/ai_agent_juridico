import requests
from requests.api import request

url = 'http://127.0.0.1:8000/execute'

print('Olá, Seja bem-vindo ao sistema de busca jurídica. Nesse projeto temos um time de IA especialista em te ajudar sobre questões jurídicas, Diga algo em que podemos te ajudar.')

pergunta = input('Digite sua pergunta: ')

payload = {
    'pergunta' : pergunta
}

print('Pensando...')

response = requests.post(
    url,
    json = payload,
    timeout = 300
)


response.raise_for_status()

dados = response.json()

print(f"🤖 Agente Jurídico : {dados['resposta']}")