from crewai import Agent, LLM, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv


load_dotenv()


def criar_crew():

    llm = LLM(
        model="openai/gpt-4o-mini"
    )

    ferramenta_pesquisa = SerperDevTool()


    pesquisador_juridico = Agent(
        role="Pesquisador Jurídico",

        goal="""
        Pesquisar e organizar informações relevantes
        sobre temas jurídicos brasileiros.
        """,

        backstory="""
        Você é um pesquisador especializado em legislação
        e jurisprudência brasileira.

        Seu trabalho é reunir informações relevantes,
        identificar conceitos jurídicos importantes e
        organizar os resultados para que outro especialista
        possa realizar uma análise jurídica.
        """,

        llm=llm,

        tools=[
            ferramenta_pesquisa
        ],

        verbose=True
    )


    agente_juridico = Agent(
        role="Assistente Jurídico",

        goal="""
        Analisar questões jurídicas e fornecer informações
        claras, objetivas e fundamentadas.
        """,

        backstory="""
        Você é um assistente especializado em Direito Brasileiro,
        com experiência em análise de legislação, contratos e
        Direito do Consumidor.
        """,

        llm=llm,

        verbose=True
    )


    tarefa_pesquisa = Task(
    description="""
    Pesquise informações confiáveis e atualizadas sobre
    a seguinte questão jurídica:

    {pergunta}

    Priorize fontes oficiais e confiáveis, como:
    - legislação brasileira;
    - sites do Governo Federal;
    - tribunais;
    - órgãos reguladores;
    - Caixa Econômica Federal;
    - Planalto;
    - JusBrasil apenas como fonte complementar.

    Para cada informação relevante, registre também
    a fonte e a URL utilizada.
    """,

    expected_output="""
    Um resumo estruturado contendo:

    1. Principais informações encontradas;
    2. Fundamentos legais;
    3. Nome das fontes consultadas;
    4. URLs das fontes utilizadas.

    Não invente URLs ou fontes.
    """,

    agent=pesquisador_juridico
    )


    tarefa_analise = Task(
    description="""
    Com base exclusivamente na pesquisa fornecida como contexto,
    responda à seguinte questão jurídica:

    {pergunta}

    Produza uma análise clara, objetiva e fundamentada.

    Não invente legislação, decisões judiciais, fontes ou URLs.

    Caso as fontes encontradas sejam insuficientes,
    informe explicitamente essa limitação.
    """,

    expected_output="""
    Produza a resposta utilizando esta estrutura:

    ## Resposta

    Explicação clara sobre a questão apresentada.

    ## Fundamentos

    Principais fundamentos jurídicos encontrados.

    ## Fontes consultadas

    Liste o nome de cada fonte e sua respectiva URL.
    """,

    agent=agente_juridico,

    context=[
        tarefa_pesquisa
    ]
    )


    crew = Crew(
        agents=[
            pesquisador_juridico,
            agente_juridico
        ],

        tasks=[
            tarefa_pesquisa,
            tarefa_analise
        ],

        process=Process.sequential,

        verbose=True
    )

    return crew

def executar_time(pergunta: str):

    crew = criar_crew()

    resultado = crew.kickoff(
        inputs={
            "pergunta": pergunta
        }
    )

    return str(resultado)