#este script tem como objetivo atualizar a lista

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv


pagina = requests.get("http://www.alepe.pe.gov.br/parlamentares/").text
obj = BeautifulSoup(pagina, 'html.parser')

objlist = obj.find('select', {'id' : 'field-deputados'}).find_all('option')

for x in objlist:
    print(x.text)

print(len(objlist))

