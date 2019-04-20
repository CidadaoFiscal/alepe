from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import datetime
from time import gmtime, strftime
import itertools

#1.0 cria lista com todos os códigos de deputados registrados no sistema da ALEPE
relatorio_cod_dep = []
lista_deputado = []

paginadeputados = requests.get("http://www.alepe.pe.gov.br/transparencia-vi/").text
objdeputados = BeautifulSoup(paginadeputados, 'html.parser').find('select', {'id' : 'selectDep'}).find_all('option')

for i in objdeputados:
    data_import = strftime('%Y-%m-%d %H:%M:%S')
    cod_dep = i['value']
    parlamentar = i.text
    relatorio_cod_dep.append((data_import,cod_dep,parlamentar))
    lista_deputado.append(cod_dep)

#1.1 Criar dataframe e exportar csv file    
dfcodigo= pd.DataFrame(relatorio_cod_dep, columns=["Data Import","Cod", "Parlamentar"])
dep_nome_csv = strftime('%Y-%m-%d %H:%M:%S')+' (codigos_deputados_alepe).csv'
dfcodigo.to_csv(dep_nome_csv, index = False, sep='|')

####################
#2.0 Código que verifica quais são as páginas que contém verbas indenizatórias para cada Deputado x Ano x Mês
#... este código serve para acelerar o processo de extração. Iremos apenas capturar dados de páginas que possuem verbas

relatorio_meses =[]

lista_ano = ['2011','2012','2013','2014','2015','2016','2017','2018','2019']
lista_meses = []
contagem_pagina = 0

for a in lista_deputado:
    pag_dep = str(a)
    for b in lista_ano:
        pag_ano = str(b)
        contagem_pagina = contagem_pagina + 1
        print(strftime('%Y-%m-%d %H:%M:%S')," (",contagem_pagina," de", len(lista_deputado)*len(lista_ano),"... ",round(contagem_pagina/len(lista_deputado)*len(lista_ano),2),"%)", pag_dep, pag_ano)
        pag_cod_link = "http://www.alepe.pe.gov.br/servicos/transparencia/adm/verbaindenizatoria-dep-meses.php?dep="+pag_dep+"&ano="+pag_ano
        meses_json = requests.get(pag_cod_link).json()
        for c in meses_json:
            pag_mes = c["mes"]
            pag_link_pagina_pedidos = "http://www.alepe.pe.gov.br/servicos/transparencia/adm/verbaindenizatoria.php?dep="+pag_dep+"&ano="+pag_ano+"&mes="+pag_mes
            pag_data_import = strftime('%Y-%m-%d %H:%M:%S')
            relatorio_meses.append((pag_data_import,pag_dep,pag_ano,pag_mes,pag_link_pagina_pedidos))
            
#Criar dataframe e exportar csv file    
dfmeses= pd.DataFrame(relatorio_meses, columns=["Data Import","Parlamentar", "Ano", "Mes", "Link Página"])
meses_nome_csv = strftime('%Y-%m-%d %H:%M:%S')+' (meses_verbaind_deputados_alepe).csv'
dfmeses.to_csv(meses_nome_csv, index = False, sep='|')

#################
# 3.0 Código para capturar os dados das páginas de pedidos

# 3.1 criação da lista de páginas de pedidos a serem visitadas

relatorio_pedidos =[]
listapaginaspedidos = []

for y in relatorio_meses:
        listapaginaspedidos.append(y[4])

# 3.2 webscraping das páginas de pedidos

contagem_pagina_pedido = 0

for d in listapaginaspedidos:
    pedido_json = requests.get(d).json()
    contagem_pagina_pedido = contagem_pagina_pedido + 1

    for e in pedido_json:
        verba_data_import = strftime('%Y-%m-%d %H:%M:%S')
        verba_docid = e['docid']
        verba_numero = e['numero']
        verba_tipo = e['tipo']
        verba_ano = e['ano']
        verba_deputado = e['deputado']
        verba_mes = e['mes']
        verba_total = e['total']
        Link_dadosnotas = "http://www.alepe.pe.gov.br/servicos/transparencia/adm/verbaindenizatorianotas.php?docid="+verba_docid
        relatorio_pedidos.append((verba_data_import,verba_docid, verba_numero, verba_tipo, verba_ano, verba_deputado, verba_mes, verba_total,Link_dadosnotas))
        print(strftime('%Y-%m-%d %H:%M:%S')," (",(contagem_pagina_pedido)," de", len(listapaginaspedidos),"...",round(contagem_pagina_pedido/len(listapaginaspedidos),2)*100,"%)", verba_deputado,verba_ano,verba_mes)

# 3.3 Criar dataframe e exportar csv file    
dfpedidos= pd.DataFrame(relatorio_pedidos, columns=["Data Import","Docid", "Número", "Tipo","Ano","Parlamentar","Mês","Total","Link_dadosnotas"])
pedidos_nome_csv = strftime('%Y-%m-%d %H:%M:%S')+' (pedidos_verbaind_deputados_alepe).csv'
dfpedidos.to_csv(pedidos_nome_csv, index = False, sep='|')    

#############

relatorio_pedidos = pd.read_csv('2019-04-19 22:49:59 (pedidos_verbaind_deputados_alepe).csv')

# 4.0 Código para capturar os dados das notas fiscais:

# 4.1 criação da lista de páginas de notas a serem visitadas
listapaginasnotas = []

for z in relatorio_pedidos:
        listapaginasnotas.append(z[8])

# 4.2 webscraping das páginas de notas

relatorio_notas = []
contagem_pagina_notas = 0

for f in listapaginasnotas:
    notas_json = requests.get(f).json()
    contagem_pagina_notas = contagem_pagina_notas + 1
    nota_docid = f.strip('http://www.alepe.pe.gov.br/servicos/transparencia/adm/verbaindenizatorianotas.php?docid=')

    for g in notas_json:
        nota_data_import = strftime('%Y-%m-%d %H:%M:%S')
        nota_rubrica = g['rubrica']
        nota_sequencial = g['sequencial']
        nota_data = g['data']
        nota_cnpj = g['cnpj']
        nota_empresa = g['empresa']
        nota_valor = g['valor']
        relatorio_notas.append((nota_data_import,nota_rubrica,nota_sequencial,nota_data,nota_cnpj,nota_empresa,nota_valor,nota_docid))
        print(strftime('%Y-%m-%d %H:%M:%S')," (",(contagem_pagina_notas)," de", len(listapaginasnotas),"...",round(contagem_pagina_notas/len(listapaginasnotas),2)*100,"%)",nota_docid)

# 4.3 Criar dataframe e exportar csv file    
dfnotas= pd.DataFrame(relatorio_notas, columns=["Data Import","Rubrica", "Sequencial", "Data","CNPJ","Empresa","Valor","Docid"])
notas_nome_csv = strftime('%Y-%m-%d %H:%M:%S')+' (notas_verbaind_deputados_alepe).csv'
dfnotas.to_csv(notas_nome_csv, index = False, sep='|')

######## Último Passo ######

# 5.0 Fazer um merge dos arquivos de Pedidos e Notas para obter apenas 1 csv consolidando todas as informações que precisamos

arquivonotas = pd.read_csv(notas_nome_csv)
arquivopedidos = pd.read_csv(pedidos_nome_csv)
merged = arquivonotas.merge(arquivopedidos, on='Docid')
relatoriofinal_nome_csv = strftime('%Y-%m-%d %H:%M:%S')+' (consolidado_verbaind_deputados_alepe).csv'
merged.to_csv(relatoriofinal_nome_csv , index=False)
