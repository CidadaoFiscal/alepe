from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

obj = BeautifulSoup(open(
"/Users/Mac/Desktop/Pedro/É Possível/Projetos/Cidadao Fiscal/Dados - ALEPE Verb. Ind./exemplopagina.htm"), 'html.parser')

objdeputados = obj.find('select', {'id' : 'selectDep'}).find_all('option')

lista_deputados=[]
for cod in objdeputados:
    codigo = cod['value']
    deputado = cod.text
    lista_deputados.append([codigo, deputado])
    print(cod['value'])

#Criar dataframe e exportar csv file    
dfdeputados = pd.DataFrame(lista_deputados, columns=["Código","Deputado"])
dfdeputados.to_csv('listadeputados.csv', index = False, sep='|')

print(len(objdeputados))





