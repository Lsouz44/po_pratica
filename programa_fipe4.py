import pandas as pd
from pulp import *

# Carregar os dados do arquivo .xlsx
df = pd.read_excel('dados_carros.xlsx')

# Definir as restrições e a função objetivo
combustiveis = ['Gasolina', 'Diesel', 'Álcool']
cambios = ['manual', 'automatic']
Pmin = 0  # Definir o valor mínimo de preço
Pmax = 9999999  # Definir o valor máximo de preço
ano_min = 2015  # Definir o ano mínimo de fabricação
potencia_max = 2.0  # Definir a potência máxima

# Filtrar os dados com base nas restrições definidas
filtered_df = df[
    (df['combustivel'].isin(combustiveis)) &
    (df['cambio'].isin(cambios)) &
    (df['preco_medio'] >= Pmin) &
    (df['preco_medio'] <= Pmax) &
    (df['ano'] >= ano_min) &
    (df['tamanho_motor'] <= potencia_max)
]

# Criar o problema de maximização
prob = LpProblem("EncontrarMelhorCarro", LpMaximize)

# Variáveis de decisão
carros = list(filtered_df.index)
carro_var = LpVariable.dicts("Carro", carros, cat='Binary')

# Função objetivo
prob += lpSum(filtered_df.loc[carro, 'tamanho_motor'] * carro_var[carro] for carro in carros)

# Restrições
for carro in carros:
    prob += carro_var[carro] <= 1  # Restrição para evitar repetição do mesmo modelo

# Resolver o problema
prob.solve()

# Imprimir os resultados
print("Status:", LpStatus[prob.status])
print("-----")
print("Os 5 melhores carros:")
for carro in carros:
    if carro_var[carro].value() == 1:
        print(f"Carro: {filtered_df.loc[carro, 'marca']} {filtered_df.loc[carro, 'modelo']}")
        print(f"Combustível: {filtered_df.loc[carro, 'combustivel']}")
        print(f"Câmbio: {filtered_df.loc[carro, 'cambio']}")
        print(f"Potência: {filtered_df.loc[carro, 'tamanho_motor']}")
        print(f"Ano: {filtered_df.loc[carro, 'ano']}")
        print(f"Preço Médio: {filtered_df.loc[carro, 'preco_medio']}")
        print("-----")
