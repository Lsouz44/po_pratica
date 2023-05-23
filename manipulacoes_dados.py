import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dados = pd.read_csv("fipe_carros-outubro-2022.csv")
columns = list(dados.columns)
print(columns)
dados.sample(6)

dados = dados[['marca', 'modelo', 'ano_modelo', 'preco_medio']]

dados['preco_medio'].replace(
    regex={r'(R\$\s)': '', r'\.': '', r'\,': '.'},
    inplace=True
)

dados['preco_medio'] = dados['preco_medio'].astype("float")
dados.sample(6)

pop = "1.0 1.4 1.6 1.8 2.0".split(" ")

def get_engine_size(modelo: str, tamanhos: list[str]=pop) -> str:
    """Encontra o padrão 'n.x' se for igual
        a algum elemento  da lista 'tamanhos'.
        Retorna NaN se não houver
    """
    pattern = r"\d{1}\.\d{1}"
    match = re.findall(pattern, modelo)
    if len(match) > 0:
        if match[0] in tamanhos:
            return match[0]
        else:
            return np.NaN
    return np.NaN

tamanho_motor = pd.DataFrame(
    dados['modelo'].map(get_engine_size)
).rename(columns={'modelo': 'tamanho_motor'})

pd.concat([
    dados[
        ['marca', 'ano_modelo', 'preco_medio']
    ],
    tamanho_motor
], axis=1).sample(10)

def separador(valor: str) -> list[str]:
    lista = valor.split()
    ano = lista[0]
    combustivel = ''.join(lista[1:])
    return ano, combustivel

ano_combustivel = pd.DataFrame(
    dados['ano_modelo'].map(separador).to_list()
)[[0, 1]]

ano_combustivel.rename(columns={0: 'ano', 1: 'combustivel'}, inplace=True)
ano_combustivel.sample(6)

ano_combustivel['combustivel'].replace("KMaGasolina", "Gasolina", inplace=True)
ano_combustivel['combustivel'].replace("KMaDiesel", "Diesel", inplace=True)
ano_combustivel['ano'].replace("Zero", "2023", inplace=True)

selecao = pd.concat(
    (dados[['marca', 'preco_medio']],
    tamanho_motor,
    ano_combustivel),
    axis=1
)
selecao.sample(6)

selecao.dropna(inplace=True)
selecao['ano'] = selecao['ano'].astype('int')
selecao['idade_anos'] = 2023 - selecao['ano']
selecao.sample(6)

"""plt.style.use('dark_background')

sns.scatterplot(
    selecao[['preco_medio', 'idade_anos']].groupby('idade_anos').mean(numeric_only=True)
)
"""
