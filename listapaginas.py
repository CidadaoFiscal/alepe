import pandas as pd
import csv

paginasdf= pd.read_csv('paginas.csv')
lista_paginas = paginasdf["coluna"].values
print(lista_paginas)
print('')
print(len(lista_paginas))

#print(lista_paginas)