# PHASE 1.0 - IMPORTING LIBRARIES

# Importing libraries
import PyPDF2
import requests
from datetime import datetime
import pandas as pd
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PHASE 1.1 - DYNAMICALLY GETTING YEAR AND MONTH

#This is a way to get the file dinamically, however, it is necessary to know when the document is published to avoid the error printing!
""" current_date = datetime.now()
year = current_date.year
month_number = current_date.month
month_list = {1: 'jan', 2: 'fev', 3: 'mar', 4:'abr', 5:'maio', 6: 'jun', 7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'} 

for i in month_list:
    if month_number == i:
        month = month_list[i]
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PHASE 1.2 - MANUAL CONTROL AS DESIRED

# These ones are for manually select the month and year!
year = '2023'
month = 'maio'

url = f'https://biblioteca.ibge.gov.br/visualizacao/periodicos/236/inpc_ipca_{year}_{month}.pdf'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PHASE 2.0 - CONFIGURING TO DOWNLOAD PDF FILE FROM URL

response = requests.get(url)


file_directory_pdf_download = r'{YOUR DIRECTORY HERE}'

if response.status_code == 200:
    file_name = f'inpc_ipca_{year}_{month}.pdf'
    with open(file_directory_pdf_download, 'wb') as file:
        file.write(response.content)
    print(f'PDF downloaded and saved as {file_name}.')
else:
    print('Error downloading the PDF file.')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PHASE 2.1 - CONFIGURING TO READ PDF FILE FROM URL

# PDF directory

directory_pdf_file = r'{YOUR DIRECTORY HERE}\ipca_data.pdf'

def extract_pdf_text(file_path):
    extracted_text = ''
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_number = len(pdf_reader.pages)
        for page in range(page_number):
            current_page = pdf_reader.pages[page]
            page_text = current_page.extract_text()
            extracted_text += page_text
    
    return extracted_text

# Extracting text from PDF file
extracted_text = extract_pdf_text(directory_pdf_file)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PHASE 2.2 - SELECTING DESIRED SNIPPET FROM PDF TEXT

# Finding Desired Snippet from the Text
start = 'VARIAÇÕES ACUMULADAS EM 12 MESES POR GRUPOS E ITENS'
end = 'Fonte: IBGE, Diretoria de Pesquisas, Coordenação de Índices de Preços,'

start_index = extracted_text.find(start)
end_index = extracted_text.find(end)

if start_index != -1 and end_index != -1:
    start_index += len(start)  


snippet = extracted_text[start_index:end_index].strip()

# print(snippet)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PHASE 3.0 - TRANSFORMING WITH PANDAS TO STRUCTURATE DATA

lines = snippet.split('\n')  # Dividing text into lines

lines.remove('IPCA - MAIO DE 2023  ')
lines.remove('IBGE | IPCA e INPC | Maio  de 202 3 |                 - 16 -  ')
lines.remove('ANO MÊS NÚMERO ÍNDICE')
lines.remove('(DEZ 93 = 100) NO 3 6 NO 12')
lines.remove('MÊS MESES MESES ANO MESES')

data = []

for line in lines:
    if line != '':
        parts = line.split()
        new_parts = parts[0:3]
        data.append(new_parts)

# Creating a DataFrame
df = pd.DataFrame(data, columns=['MONTH_YEAR', 'IPCA', 'LEFTOVERS'])


# Creating column MONTH
months = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

for i in range(0, len(df)):
    if df.loc[i, 'IPCA'] in months:
        df.loc[i, 'MONTH'] = df.loc[i, 'IPCA']

    if df.loc[i, 'MONTH_YEAR'] in months:
        df.loc[i, 'MONTH'] = df.loc[i, 'MONTH_YEAR']


# Creating starting year variable
starting_year = df.loc[0, 'MONTH_YEAR']
starting_year_int = int(starting_year)

# Creating column YEAR
for i in range(1, len(df)):
    if df.loc[i, 'MONTH'] == 'JAN':
        starting_year_int += 1
    df.loc[i, 'YEAR'] = starting_year_int

df.at[0, 'YEAR'] = int(starting_year)


# Creating column IPCA_VALUE
for i in range(0, len(df)+2):
    if df.loc[i, 'IPCA'] == 'JAN':
        df.loc[i, 'IPCA_VALUE'] = df.loc[i, 'LEFTOVERS']
    else:
       df.loc[i, 'IPCA_VALUE'] = df.loc[i, 'IPCA']


# Remove unecessary columns
colunas_para_remover = ['MONTH_YEAR', 'IPCA', 'LEFTOVERS']
df = df.drop(colunas_para_remover, axis=1)


# Saving as CSV file
df.to_csv('{YOUR DIRECTORY HERE}\\ipca_data.csv', index=False, columns=['YEAR', 'MONTH', 'IPCA_VALUE'])


