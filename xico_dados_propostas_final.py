import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests
import csv

#criar a lista que será utilizada para armanezar os dados relevantes
relatorio_propostas = []
numero_extracao = 0
#Importa o csv com a lista de todas as páginas a serem extraidas
paginaspropostasdf= pd.read_csv('paginas_propostas.csv')
lista_paginas_propostas = paginaspropostasdf["link"].values

"""
#TESTE
pagina = requests.get("http://www.alepe.pe.gov.br/proposicao-texto-completo/?docid=066D1FA21E3FAE5A032582F10073A6F4").text
obj = BeautifulSoup(pagina, 'html.parser')
textocompleto = str(obj.find_all("div", {"class":"proposicao-list-item-text"})[0])
print(textocompleto)
print(type(textocompleto))
print(len(textocompleto))

#FIM DO TESTE
"""

#Extrai o conteúdo da página
for x in lista_paginas_propostas:
    numero_extracao = numero_extracao + 1
    pagina = requests.get(x).text
    obj = BeautifulSoup(pagina, 'html.parser')
#conteúdo da proposta de lei
    linkproposta = x
    titulo = obj.find("div", {"class":"proposicao-list-header"}).h2.text
    print("(",numero_extracao,"de",len(lista_paginas_propostas),")", titulo)


#Checar se existe a info "Justificativa":
    if len(obj.find_all("div", {"class":"proposicao-list-item"}))<4:
        resumo = tuple(obj.find("div", {"class":"proposicao-list-header"}).p)
        textocompleto = tuple(obj.find_all("div", {"class":"proposicao-list-item-text"})[0])
        justificativa = "nenhum"
        historico = tuple(obj.find_all("div", {"class":"proposicao-list-item-text"})[1])
    else:
        resumo = tuple(obj.find("div", {"class":"proposicao-list-header"}).p)
        textocompleto = tuple(obj.find_all("div", {"class":"proposicao-list-item-text"})[0])
        justificativa = tuple(obj.find_all("div", {"class":"proposicao-list-item-text"})[1])
        historico = tuple(obj.find_all("div", {"class":"proposicao-list-item-text"})[2])

#dados de situação e aprovações 
    situacao = obj.find_all("table", {"class":"table table-proposicao"})[0].tbody.find_all('td')[1].text
    localizacao = obj.find_all("table", {"class":"table table-proposicao"})[0].tbody.find_all('td')[3].text
#tramitação
    primeira_publicacao_data = obj.find_all("table", {"class":"table table-proposicao"})[1].tbody.find_all('td')[1].text
    primeira_publicacao_OD_data = obj.find_all("table", {"class":"table table-proposicao"})[1].tbody.find_all('tr')[1].find_all('td')[1].text
#sessão plenária
    sec_plenario_primeira_resultado = obj.find_all("table", {"class":"table table-proposicao"})[2].tbody.find_all('tr')[0].find_all('td')[1].text
    sec_plenario_primeira_data = obj.find_all("table", {"class":"table table-proposicao"})[2].tbody.find_all('tr')[0].find_all('td')[3].text
    sec_plenario_segunda_resultado = obj.find_all("table", {"class":"table table-proposicao"})[2].tbody.find_all('tr')[1].find_all('td')[1].text
    sec_plenario_segunda_data = obj.find_all("table", {"class":"table table-proposicao"})[2].tbody.find_all('tr')[1].find_all('td')[3].text
#resultado final
    redacao_final_data = obj.find_all("table", {"class":"table table-proposicao"})[3].tbody.find_all('tr')[0].find_all('td')[1].text
    redacao_final_resultado = obj.find_all("table", {"class":"table table-proposicao"})[3].tbody.find_all('tr')[2].find_all('td')[1].text
    redacao_final_resultado_data = obj.find_all("table", {"class":"table table-proposicao"})[3].tbody.find_all('tr')[2].find_all('td')[3].text


#contar o número de documentos relacionados:
    try:
        checardocumentos = obj.find("div", {"class":"msg-aviso"})["class"][0]
    except:
        checardocumentos = "existem documentos"

    if checardocumentos == "msg-aviso":
        numero_linhas_documentos = 0
    else:
        numero_linhas_documentos = len(obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr'))

#extrair os dados de documentos relacionados:

#Primeira linha
    if numero_linhas_documentos > 0:
        doc_um_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[0].find_all('td')[0].text
        doc_um_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[0].find_all('td')[1].text
        doc_um_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[0].find_all('td')[2].text
        doc_um_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[0].find_all('td')[1].a['href']
    else:
        doc_um_tipo = "nenhum"
        doc_um_numero = "nenhum"
        doc_um_autor = "nenhum"
        doc_um_link = "nenhum"

#segunda linha
    if numero_linhas_documentos > 1:
        doc_dois_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[1].find_all('td')[0].text
        doc_dois_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[1].find_all('td')[1].text
        doc_dois_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[1].find_all('td')[2].text
        doc_dois_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[1].find_all('td')[1].a['href']
    else:
        doc_dois_tipo = "nenhum"
        doc_dois_numero = "nenhum"
        doc_dois_autor = "nenhum"
        doc_dois_link = "nenhum"

#terceira linha
    if numero_linhas_documentos > 2:
        doc_tres_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[2].find_all('td')[0].text
        doc_tres_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[2].find_all('td')[1].text
        doc_tres_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[2].find_all('td')[2].text
        doc_tres_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[2].find_all('td')[1].a['href']
    else:
        doc_tres_tipo = "nenhum"
        doc_tres_numero = "nenhum"
        doc_tres_autor = "nenhum"
        doc_tres_link = "nenhum"

#quarta linha
    if numero_linhas_documentos > 3:
        doc_quarta_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[3].find_all('td')[0].text
        doc_quarta_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[3].find_all('td')[1].text
        doc_quarta_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[3].find_all('td')[2].text
        doc_quarta_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[3].find_all('td')[1].a['href']
    else:
        doc_quarta_tipo = "nenhum"
        doc_quarta_numero = "nenhum"
        doc_quarta_autor = "nenhum"
        doc_quarta_link = "nenhum"

#quinta linha
    if numero_linhas_documentos > 4:
        doc_quinta_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[4].find_all('td')[0].text
        doc_quinta_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[4].find_all('td')[1].text
        doc_quinta_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[4].find_all('td')[2].text
        doc_quinta_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[4].find_all('td')[1].a['href']
    else:
        doc_quinta_tipo = "nenhum"
        doc_quinta_numero = "nenhum"
        doc_quinta_autor = "nenhum"
        doc_quinta_link = "nenhum"

#sexta linha
    if numero_linhas_documentos > 5:
        doc_sexta_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[5].find_all('td')[0].text
        doc_sexta_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[5].find_all('td')[1].text
        doc_sexta_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[5].find_all('td')[2].text
        doc_sexta_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[5].find_all('td')[1].a['href']
    else:
        doc_sexta_tipo = "nenhum"
        doc_sexta_numero = "nenhum"
        doc_sexta_autor = "nenhum"
        doc_sexta_link = "nenhum"

#setima linha
    if numero_linhas_documentos > 6:
        doc_setima_tipo = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[6].find_all('td')[0].text
        doc_setima_numero = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[6].find_all('td')[1].text
        doc_setima_autor = obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[6].find_all('td')[2].text
        doc_setima_link = "http://www.alepe.pe.gov.br" + obj.find_all("table", {"class":"table"})[-1].tbody.find_all('tr')[6].find_all('td')[1].a['href']
    else:
        doc_setima_tipo = "nenhum"
        doc_setima_numero = "nenhum"
        doc_setima_autor = "nenhum"
        doc_setima_link = "nenhum"

    relatorio_propostas.append((
    linkproposta,
    titulo,
    resumo,
    textocompleto,
    justificativa,
    historico,
    situacao,
    localizacao,
    primeira_publicacao_data,
    primeira_publicacao_OD_data,
    sec_plenario_primeira_resultado,
    sec_plenario_primeira_data,
    sec_plenario_segunda_resultado,
    sec_plenario_segunda_data,
    redacao_final_data,
    redacao_final_resultado,
    redacao_final_resultado_data,
    numero_linhas_documentos,
    doc_um_tipo,
    doc_um_numero,
    doc_um_autor,
    doc_um_link,
    doc_dois_tipo,
    doc_dois_numero,
    doc_dois_autor,
    doc_dois_link,
    doc_tres_tipo,
    doc_tres_numero,
    doc_tres_autor,
    doc_tres_link,
    doc_quarta_tipo,
    doc_quarta_numero,
    doc_quarta_autor,
    doc_quarta_link,
    doc_quinta_tipo,
    doc_quinta_numero,
    doc_quinta_autor,
    doc_quinta_link,
    doc_sexta_tipo,
    doc_sexta_numero,
    doc_sexta_autor,
    doc_sexta_link,
    doc_setima_tipo,
    doc_setima_numero,
    doc_setima_autor,
    doc_setima_link,
    ))

#Criar dataframe e exportar csv file    
dfpropostas = pd.DataFrame(relatorio_propostas,columns=[
"linkproposta",
"titulo",
"resumo",
"textocompleto",
"justificativa",
"historico",
"situacao",
"localizacao",
"primeira_publicacao_data",
"primeira_publicacao_OD_data",
"sec_plenario_primeira_resultado",
"sec_plenario_primeira_data",
"sec_plenario_segunda_resultado",
"sec_plenario_segunda_data",
"redacao_final_data",
"redacao_final_resultado",
"redacao_final_resultado_data",
"numero_linhas_documentos",
"doc_um_tipo",
"doc_um_numero",
"doc_um_autor",
"doc_um_link",
"doc_dois_tipo",
"doc_dois_numero",
"doc_dois_autor",
"doc_dois_link",
"doc_tres_tipo",
"doc_tres_numero",
"doc_tres_autor",
"doc_tres_link",
"doc_quarta_tipo",
"doc_quarta_numero",
"doc_quarta_autor",
"doc_quarta_link",
"doc_quinta_tipo",
"doc_quinta_numero",
"doc_quinta_autor",
"doc_quinta_link",
"doc_sexta_tipo",
"doc_sexta_numero",
"doc_sexta_autor",
"doc_sexta_link",
"doc_setima_tipo",
"doc_setima_numero",
"doc_setima_autor",
"doc_setima_link",
])

dfpropostas.to_csv('report_dados_propostas.csv', index = False, sep='|')



