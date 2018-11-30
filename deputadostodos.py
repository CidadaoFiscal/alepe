#este script tem como objetivo atualizar a lista

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv


#cria lista com todos os deputados que já ocuparam a ALEPE
paginadeputados = requests.get("http://www.alepe.pe.gov.br/transparencia-vi/").text
objdeputados = BeautifulSoup(paginadeputados, 'html.parser')
listadeputados = objdeputados.find('select', {'id' : 'selectDep'}).find_all('option')

for deputado in listadeputados:
    print(deputado.text)

print("")
print(len(listadeputados))



