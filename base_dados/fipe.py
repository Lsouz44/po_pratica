import numpy as np
import pandas as pd
from process import process_data

file_path = "fipe_carros-outubro-2022.csv"
data = process_data(file_path)
data.to_excel('~/Documentos/po_pratica/tabela_nova.xlsx', index=False) # Salvar o DataFrame em um arquivo Excel
data.sample(6)