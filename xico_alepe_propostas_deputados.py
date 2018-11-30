import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests

#cria lista com todos os deputados que já ocuparam a ALEPE
paginadeputados = requests.get("http://www.alepe.pe.gov.br/transparencia-vi/").text
objdeputados = BeautifulSoup(paginadeputados, 'html.parser').find('select', {'id' : 'selectDep'}).find_all('option')[1:]
listadeputados = []

for dep in objdeputados:
    listadeputados.append(dep.text)
    
#cria a lista que será utilizada para armazenar os dados relevantes
relatorio_propostas = []

#abrir a primeira página
driver = webdriver.Chrome('/Users/Mac/Desktop/Pedro/chromedriver')
driver.get('http://www.alepe.pe.gov.br/proposicoes/#')

#Selecionar os parâmetros da página
for deputado in listadeputados:
    
    selecioneprojeto = driver.find_element_by_id('field-tipo-filtro')
    selecioneprojeto.send_keys('projetos')

    selecionetipo = driver.find_element_by_id('field-proposicoes-filtro2')
    selecionetipo.send_keys('Por autor')

    selecionenome = driver.find_element_by_id('field-proposicoes2')
    selecionenome.clear()
    selecionenome.send_keys(deputado)
    driver.find_elements_by_css_selector("a.button")[0].click()

    #time.sleep(3)

    #Extrair o conteúdo HTML da primeira página
    doc = driver.page_source
    soup = BeautifulSoup(doc, 'html.parser')

    try:
        results = soup.find('tbody').find_all('tr')
    
        #Salvar os dados em uma tabela
        for x in results:
            autor = x.contents[1].text
            proposicao = x.contents[5].text
            data = x.contents[7].text
            link = "http://www.alepe.pe.gov.br" + x.contents[5].a['href']
            relatorio_propostas.append([autor, proposicao, data, link])

        #Repetir o mesmo trabalho para todas as outras páginas

        try:
            time.sleep(3)
            numerodepaginas = int(soup.find('div', {'class':'pages'}).find_all('a')[-1].text)
            proximapagina = 2
            listapaginas = list(range(proximapagina, numerodepaginas+1))

            for pag in listapaginas:
                driver.find_element_by_link_text(str(pag)).click()
                #time.sleep(3)
    
                #Extrair o conteúdo HTML da segunda página
                doc = driver.page_source
                soup = BeautifulSoup(doc, 'html.parser')
                results = soup.find('tbody').find_all('tr')

                #Salvar os dados em uma tabela
                for x in results:
                    autor = x.contents[1].text
                    proposicao = x.contents[5].text
                    data = x.contents[7].text
                    link = "http://www.alepe.pe.gov.br" + x.contents[5].a['href']
                    relatorio_propostas.append([autor, proposicao, data, link])

        except:
            pass

    except:
        pass


#salvar a lista em um arquivo .csv
dfpropostas = pd.DataFrame(relatorio_propostas, columns=["Autor","Proposta de Lei","Data","Link"])
dfpropostas.to_csv('reportpropostas.csv', index = False, sep='|')

#time.sleep(5)
driver.quit()