from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import datetime
from time import gmtime, strftime

#Cria as listas que serão exportadas para csv (Este é o produto final deste algorithm)
relatorio_verbas = []
relatorio_pedidos = []
numeropagina = 0

#Importa o csv com a lista de todas as páginas a serem extraidas
paginasdf= pd.read_csv('paginas.csv')
lista_paginas = paginasdf["coluna"].values

#Extrair conteúdo de todas as paginas listadas na variavel 'lista_paginas'
for a in lista_paginas:
    pagina = requests.get(a).text
    obj = BeautifulSoup(pagina, 'html.parser')


#Extrair nome do deputado e período + zera o index tabela (este index é utilizado para mostrar
# a ordem na qual as despesas aparecem no site. Isto servirá para linkar depesa com código do pedido via EXCEL)
#Incluir Try / Except para desconsiderar links inválidos ou deputados sem registro de verba indenizatória no período
    indexverbas = 0
    indexpedidos = 0
    
    try:
        nomedeputado = obj.find('div', {'class': 'search-result-resume'}).find('strong', {'class':'query'}).text
        periodo = obj.find('div', {'class': 'search-result-resume'}).find('strong', {'class':'numbers'}).text
        numeropagina = numeropagina + 1
        print(strftime("%Y-%m-%d %H:%M:%S"),"(",numeropagina,"out of",len(lista_paginas),")",nomedeputado, periodo)

#Obter o objeto de beautifulsoup onde estão localizados os tags de # pedido, tipo de despesa e valores dos gastos 
        objlist = obj.find('div', {'id' : 'div-com-verba'}).find_all('div', {'class' : 'accordion'})
    
        obj_pedidos = objlist[0].parent.find_all('h2')

#Extrair o código dos pedidos
        for x in obj_pedidos:
            pedido = x.text
            indexpedidos = indexpedidos + 1
            relatorio_pedidos.append((indexpedidos, nomedeputado, periodo, pedido))

#Extrair o tipo de despesa + conteúdo das tabelas
        for i in objlist:
            tipodespesa = i.h4.text.strip()    
            listatabela = i.find('table', {'class' : 'table'}).find_all('tbody')

            for item in listatabela:
                date = item.contents[1].text
                cnpj = item.contents[3].text
                empresa = item.contents[5].text
                valor = item.contents[7].text
                indexverbas = indexverbas + 1
                relatorio_verbas.append((indexverbas, nomedeputado, periodo, tipodespesa, date, cnpj, empresa, valor))
    except:
        numeropagina = numeropagina + 1
        print(strftime("%Y-%m-%d %H:%M:%S"),"(",numeropagina,"out of",len(lista_paginas),")"," ", a)
        pass


#Criar dataframe e exportar csv file    
dfverbas = pd.DataFrame(relatorio_verbas, columns=["Index Verbas", "Parlamentar", "Período","Tipo Despesa", "Data", "CNPJ", "Empresa", "Valor"])
dfverbas.to_csv('reportverbas.csv', index = False, sep='|')

dfpedidos = pd.DataFrame(relatorio_pedidos, columns=["index Pedidos", "Parlamentar", "Período", "Pedido"])
dfpedidos.to_csv('reportpedidos.csv', index = False, sep='|')

print(datetime.datetime.now())