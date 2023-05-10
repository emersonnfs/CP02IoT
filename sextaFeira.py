import random
import speech_recognition as sr
import os
from gtts import gTTS
from playsound import playsound
import requests
import json
from googlesearch import search
import webbrowser
import wikipedia
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from google.cloud import translate_v3 as translate

def falar(resposta):
    num_aleatorio = random.randint(1, 100000)
    nome_arquivo = f"resposta{num_aleatorio}.mp3"
    audio = gTTS(resposta, lang='pt')
    audio.save(nome_arquivo)
    playsound(nome_arquivo)
    os.remove(nome_arquivo)

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic)
        print("Diga algo...")
        audio = r.listen(mic)
    try:
        comando = r.recognize_google(audio, language='pt')
        print("Você disse: " + comando)
    except sr.UnknownValueError:
        falar("Não entendi o que você disse")
        comando = ""
    return comando

def cadastrar_na_agenda():
    falar("Que evento deseja cadastrar na agenda?")
    novo_comando = ouvir_comando()
    with open("TesteCp2Agenda.txt", "a") as arquivo:
        arquivo.write("\n" + novo_comando)
    falar("Cadastrando evento na agenda...")

def ler_agenda():
    falar("Abrindo agenda...")
    with open("TesteCp2Agenda.txt","r") as arquivo:
        for linha in arquivo:
            falar(linha)
        falar("Foram lidos todos os eventos da agenda")

def obter_previsao_do_tempo():
    falar("Que cidade gostaria de saber a previsão do tempo?")
    cidade = ouvir_comando()
    chave_api = "f7f2d4d39c0a07b7394ee46378e19096"
    cidade_formatada = cidade.replace(" ", "%20")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade_formatada}&appid={chave_api}&lang=pt_br&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        dados = json.loads(response.content)
        clima = dados["weather"][0]["description"]
        temperatura = dados["main"]["temp"]
        umidade = dados["main"]["humidity"]
        falar(f"Previsão do tempo para {cidade}: {clima}. Temperatura: {temperatura}°C. Umidade: {umidade}%")
    else:
        falar("Erro ao obter a previsão do tempo.")

def pesquisar_no_google():
    falar("O que deseja pesquisar?")
    novo_comando = ouvir_comando()
    for result in search(novo_comando, num_results=1):
        falar("Aqui está o primeiro site do google que satisfaz a sua pesquisa.")
        webbrowser.open(result)
        break
    falar("Aperte enter para voltar para assistente")
    input("Aperte enter para voltar para assistente")

def pesquisar_wikipedia():
    falar("O que deseja pesquisar na Wikipedia?")
    novo_comando = ouvir_comando()
    try:
        wikipedia.set_lang("pt")
        resultado = wikipedia.summary(novo_comando, sentences=2)
        falar(resultado)
    except wikipedia.exceptions.DisambiguationError as e:
        falar("Por favor, seja mais específico em sua pesquisa.")
    except wikipedia.exceptions.PageError as e:
        falar("Não foi possível encontrar informações sobre o tópico pesquisado.")

def obter_sugestao_filme():
    falar("Carregando")
    print("Carregando...")
    chave_api = "d6849e821cbc407ccc20f04b99edb233"
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={chave_api}&language=pt-BR&sort_by=popularity.desc&include_adult=false&include_video=false&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        dados = json.loads(response.content)
        resultados = dados["results"]
        filme_aleatorio = random.choice(resultados)
        titulo = filme_aleatorio["title"]
        descricao = filme_aleatorio["overview"]
        falar(f"Eu sugiro o filme {titulo}. Aqui está uma breve descrição: {descricao}")
    else:
        falar("Desculpe, não foi possível obter uma sugestão de filme no momento.")


def sugerir_livro():
    falar("Carregando")
    print("Carregando...")
    chave_api = "AIzaSyBXiZDqG44X5kzWFm-VZ6UY8hA5cEfbEZ8"

    parametros = {
        'q': 'livro aleatorio',
        'maxResults': 10,
        'key': chave_api
    }

    url = 'https://www.googleapis.com/books/v1/volumes'

    try:
        response = requests.get(url, params=parametros)
        if response.status_code == 200:
            dados = response.json()
            livros = dados['items']

            if livros:
                livro_sugerido = random.choice(livros)
                titulo = livro_sugerido['volumeInfo']['title']

                if 'authors' in livro_sugerido['volumeInfo']:
                    autores = livro_sugerido['volumeInfo']['authors']
                else:
                    autores = ['Autor Desconhecido']
                if 'descrition' in livro_sugerido['volumeInfo']:
                    descricao = livro_sugerido['volumeInfo']['description']
                else:
                    descricao = ['Não possui descrição']

                mensagem = f"Aqui está uma sugestão de livro para você: '{titulo}' de {', '.join(autores)}."
                mensagem += f"\nDescrição: {descricao}"
                falar(mensagem)
            else:
                falar("Desculpe, não foi possível encontrar sugestões de livros no momento.")
        else:
            falar("Erro ao obter sugestões de livros. Por favor, tente novamente mais tarde.")
    except requests.exceptions.RequestException:
        falar("Ocorreu um erro de conexão. Verifique sua conexão com a internet e tente novamente.")

    falar("Aperte enter para voltar para assistente")
    input("Aperte enter para voltar para assistente")


def obter_piada():
    url = "https://sv443.net/jokeapi/v2/joke/Any?lang=pt"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = json.loads(response.content)
            if dados['type'] == 'single':
                piada = dados['joke']
            elif dados['type'] == 'twopart':
                piada = f"{dados['setup']} {dados['delivery']}"
            else:
                piada = "Não foi possível obter a piada."

            falar(piada)
        else:
            falar("Erro ao obter piada. Por favor, tente novamente mais tarde.")
    except requests.exceptions.RequestException:
        falar("Ocorreu um erro de conexão. Verifique sua conexão com a internet e tente novamente.")

def pesquisar_no_youtube():
    falar("Quer ver um vídeo sobre qual assunto?")
    pesquisa=ouvir_comando()
    API_KEY="AIzaSyBSKWoAgLPRxolLC-YzUF7VxoywtMIKAss"
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        request = youtube.search().list(
            q=pesquisa,
            part='id',
            maxResults=1,
            type='video'
        )
        response = request.execute()

        if 'items' in response:
            if len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                falar("Abrindo o vídeo")
                print("Carregando...")
                webbrowser.open(video_url)
        else:
            falar("Nenhum vídeo encontrado.")
        falar("Aperte enter para voltar para assistente")
        input("Aperte enter para voltar para assistente")
    except HttpError as e:
        print(f'Erro ao fazer a pesquisa no YouTube: {e}')
        falar("Erro ao fazer a pesquisa no YouTube.")

input("aperte enter para começar.")
while True:
    comando = ouvir_comando()
    if 'ok sexta-feira' in comando:
        resp="Sim, mestre. O que posso fazer?"
        falar(resp)
        while True:
            novo_comando = ouvir_comando()
            #01-CADASTRAR EVENTO NA AGENDA
            if 'cadastrar evento na agenda' in novo_comando:
                cadastrar_na_agenda()
                break
            #02-LER AGENDA
            elif 'ler agenda' in novo_comando:
                ler_agenda()
                break
            #03-PREVISÃO DO TEMPO
            elif 'previsão do tempo' in novo_comando:
               obter_previsao_do_tempo()
               break
            #04-PESQUISAR NO GOOGLE
            elif 'pesquisar no Google' in novo_comando:
                pesquisar_no_google()
                break
            #05-PESQUISAR NO WIKIPEDIA
            elif 'pesquisar no Wikipédia' in novo_comando:
                pesquisar_wikipedia()
                break
            #06-SUGERIR UM FILME
            elif 'sugere um filme' in novo_comando:
                obter_sugestao_filme()
                break
            #07-SUGERIR UM LIVRO
            elif 'sugere um livro' in novo_comando:
                sugerir_livro()
                break
            #08-CONTAR UMA PIADA
            elif 'conta uma piada' in novo_comando:
                obter_piada()
                break
            #09-PESQUISAR NO YOUTUBE
            elif 'pesquisar no YouTube' in novo_comando:
                pesquisar_no_youtube()
                break
            #10-
            else:
                falar("Ops, não entendi esse comando fale novamente.")
    elif 'desligar sexta-feira' in comando:
        falar("Tamo junto mestre. Precisando é só da play nessa budega de cima")
        break