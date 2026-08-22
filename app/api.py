from fastapi import FastAPI
from pydantic import BaseModel

from app.crew import executar_time

app = FastAPI(
    title = 'API Agente Juridico',
    version = '1.0.0'
)

class PerguntaRequest(BaseModel):
    pergunta : str

@app.get('/')
def health_check():
    return {
        'status' : 'online'
    }

@app.post('/execute')
def executar_agente(request: PerguntaRequest):
    resposta = executar_time(
        request.pergunta
    )

    return {
        'pergunta' : request.pergunta,
        'resposta' : resposta
        }
