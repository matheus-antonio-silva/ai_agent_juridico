from crewai import Agent, LLM, Task,Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv


# Carregando variáveis de ambiente
load_dotenv()

# Definindo a tool de pesquisa
ferramenta_pesquisa = SerperDevTool()


# Definindo o modelo padrao do LLM
llm = LLM(
    model = 'openai/gpt-4o-mini'
)

# Criando o agente de ia juridico
agente_juridico = Agent(
    role = 'Assistente Jurídico',
    goal = """
    Analisar questões jurídicas e fornecer informações
    claras, objetivos e fundamentadas.
    """,
    backstory = """
    Você é um assistente especializado em Direito Brasileiro,
    com experiência em análise de legislação, contratos e
    questões relacionadas ao Direito do Consumidor.
    """,
    llm = llm,
    verbose = True
)

# Criando o segundo agente de IA
agente_pesquisador_juridico = Agent(
    role = 'Pesquisador Jurídico',
    goal = """
    Pesquisar e organizar informações relevantes
    sobre temas jurídicos brasileiros.
    """,
    backstory = """
    Você é um pesquisador especializado em legislação
    e jurisprudência brasileira.

    Seu trabalho é reunir informações relevantes,
    identificar conceitos jurídicos importantes e
    organizar os resultados para que outro especialista
    possa realizar uma análise jurídica.
    """,
    llm = llm,
    verbose = True,
    tools = [ferramenta_pesquisa]
)

# Definindo a task do agente

tarefa_pesquisa = Task(
    description="""
    Pesquise informações confiáveis e atualizadas sobre
    a seguinte questão jurídica:

    {pergunta}

    Organize os principais conceitos, fundamentos legais
    e informações relevantes encontradas.
    """,
    expected_output="""
    Um resumo estruturado com as principais informações
    encontradas sobre a questão apresentada.
    """,
    agent = agente_pesquisador_juridico
)

tarefa_analise = Task(
    description="""
    Com base na pesquisa realizada, responda à seguinte
    questão jurídica:

    {pergunta}

    Produza uma análise clara, objetiva e fundamentada.
    """,
    expected_output="""
    Uma resposta jurídica clara e estruturada,
    contendo os fundamentos relevantes encontrados
    durante a pesquisa.
    """,
    agent = agente_juridico,
    context=[tarefa_pesquisa]
)

# Criando o time de agentes
crew_juridica = Crew(
    agents = [agente_juridico,agente_pesquisador_juridico],
    tasks=[
        tarefa_pesquisa,
        tarefa_analise],
    verbose=True,
    process = Process.sequential
)


if __name__ == "__main__":

    pergunta_usuario = input("Digite sua pergunta: ")

    if not pergunta_usuario:
        print('Digite uma pergunta para o Agente')

    resultado = crew_juridica.kickoff(
        inputs = {
            "pergunta" : pergunta_usuario
        }
    )

    print(resultado)