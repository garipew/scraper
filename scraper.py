from selenium import webdriver
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from datetime import datetime
import os

def extrair_status(reclamacao_div):
    possible_classes = ["sc-1a60wwz-1 cojagP",
                       "sc-1a60wwz-1 eSyZEo",
                       "sc-1a60wwz-1 zBBWP",
                       "sc-1a60wwz-1 loLKap",
                       "sc-1a60wwz-1 gLuDFD"]
    for classe in possible_classes:
        status_span = reclamacao_div.find("span", class_=classe)
        if status_span != None:
            break
    return status_span.text

def extrair_titulo(reclamacao_div):
    titulo_classe = "sc-lzlu7c-3 hnjYTW"
    titulo_tag = reclamacao_div.find("h1", class_=titulo_classe)
    return titulo_tag.text

def extrair_local(reclamacao_div):
    local_classe = "sc-lzlu7c-6 sc-lzlu7c-7 wFAth hVBZZt"
    local_div = reclamacao_div.find("div", class_=local_classe)
    local_span = local_div.find("span")
    return local_span.text

def extrair_data(reclamacao_div):
    data_classe = "sc-lzlu7c-6 sc-lzlu7c-8 wFAth biGvqa"
    data_div = reclamacao_div.find("div", class_=data_classe)
    data_span = data_div.find("span")
    return data_span.text

def extrair_texto(reclamacao_div):
    texto_classe = "sc-lzlu7c-17 fRVYjv"
    texto_tag = reclamacao_div.find("p", class_=texto_classe)
    return texto_tag.text

def extrair_dados(reclamacao):
    link = reclamacao.find("a")
    if not link:
        return
    reclamacao_url = link.get("href")
    reclamacao_url = root + reclamacao_url
    driver.get(reclamacao_url)

    start = datetime.now().timestamp()

    time.sleep(5)
    reclamacao_html = driver.page_source

    reclamacao_soup = BeautifulSoup(reclamacao_html, "html.parser")
    reclamacao_classe = "sc-lzlu7c-19 ijjgZd"
    reclamacao_div = reclamacao_soup.find("div", class_=reclamacao_classe)

    titulo = extrair_titulo(reclamacao_div)
    local = extrair_local(reclamacao_div)
    status = extrair_status(reclamacao_div)
    data = extrair_data(reclamacao_div)
    texto = extrair_texto(reclamacao_div)

    return {"titulo": titulo,
        "local": local,
        "data": data,
        "status": status,
        "texto": texto 
        },start

def extrair_reclamacoes(reclamacoes):
    for reclamacao in reclamacoes:
        dados,start = extrair_dados(reclamacao)
        if dados == None:
            continue
        df = pd.DataFrame([dados])
        if os.path.exists(output):
            pd.concat([pd.read_csv(output), df]).to_csv(output, index=False)
        else:
            df.to_csv(output, index=False)
        print(f"""
===============================================================
Reclamação salva!
    titulo: {dados["titulo"]}
    local: {dados["local"]}
    status: {dados["status"]}
    data: {dados["data"]}
===============================================================""")

        end = datetime.now().timestamp()
        elapsed = end - start
        if elapsed < CRAWL_DELAY:
            print(f"Aguardando delay de {CRAWL_DELAY-elapsed}s")
            time.sleep(CRAWL_DELAY - elapsed + random.uniform(0, 1))


CRAWL_DELAY = 10 # NÂO MUDA ISSO
elapsed = 0

driver = uc.Chrome()

root = "https://www.reclameaqui.com.br"
reclamacoes_classe = "sc-1pe7b5t-0 eJgBOc"

output = "reclameaqui.csv"

paginas = range(25, 51)
for pagina in paginas:
    url = f'https://www.reclameaqui.com.br/empresa/byd-do-brasil/lista-reclamacoes/?pagina={pagina}'
    driver.get(url)
    time.sleep(CRAWL_DELAY)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    reclamacoes = soup.find_all("div", class_=reclamacoes_classe)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Analisando página {pagina}.")
    print(f"Existem {len(reclamacoes)} reclamacoes aqui.")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    extrair_reclamacoes(reclamacoes)
