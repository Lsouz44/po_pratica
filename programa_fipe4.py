import pandas as pd
from pulp import *

# Carregando os dados do arquivo .xlsx
data = pd.read_excel('dados_carros.xlsx')

# Criação do problema de maximização
prob = LpProblem("Seleção de Carros", LpMaximize)

# Criando as variáveis de decisão
carros = list(data.index)
carro_selecionado = LpVariable.dicts("CarroSelecionado", carros, cat='Binary')

# Definindo a função objetivo
potencia = dict(zip(carros, data['tamanho_motor']))
prob += lpSum(potencia[i] * carro_selecionado[i] for i in carros)

# Definindo as restrições
combustivel_restricao = 'Gasolina'  # Defina o combustível desejado
cambio_restricao = 'manual'  # Defina o câmbio desejado
preco_min = 10000  # Defina o preço mínimo desejado
preco_max = 50000  # Defina o preço máximo desejado
ano_min = 2015  # Defina o ano mínimo desejado
potencia_max = 2.0  # Defina a potência máxima desejada

for i in carros:
    # Restrição de combustível
    if data.loc[i, 'combustivel'] != combustivel_restricao:
        prob += carro_selecionado[i] == 0
    
    # Restrição de câmbio
    if data.loc[i, 'cambio'] != cambio_restricao:
        prob += carro_selecionado[i] == 0
    
    # Restrição de faixa de preço
    if not preco_min <= data.loc[i, 'preco_medio'] <= preco_max:
        prob += carro_selecionado[i] == 0
    
    # Restrição de ano de fabricação
    if data.loc[i, 'ano'] < ano_min:
        prob += carro_selecionado[i] == 0
    
    # Restrição de potência máxima
    if data.loc[i, 'tamanho_motor'] > potencia_max:
        prob += carro_selecionado[i] == 0
    
    # Restrição para não repetir o mesmo modelo
    modelo = data.loc[i, 'modelo']
    prob += lpSum(carro_selecionado[j] for j in carros if data.loc[j, 'modelo'] == modelo) <= 1

# Restrição para retornar apenas um modelo por marca (opcional)
marcas_selecionadas = set()  # Preencha com as marcas desejadas separadas por vírgula
for i in carros:
    marca = data.loc[i, 'marca']
    if marcas_selecionadas and marca not in marcas_selecionadas:
        prob += carro_selecionado[i] == 0

# Definindo o número máximo de carros a serem selecionados
num_carros_selecionados = 5
prob += lpSum(carro_selecionado[i] for i in carros) == num_carros_selecionados

# Resolvendo o problema
prob.solve()

# Extraindo a lista de carros selecionados
carros_selecionados = [i for i in carros if carro_selecionado[i].varValue == 1]

# Imprimindo os resultados
print("Lista dos 5 melhores carros selecionados:")
for i in carros_selecionados:
    print(f"Carro: {data.loc[i, 'marca']} {data.loc[i, 'modelo']}")
    print(f"Potência: {data.loc[i, 'tamanho_motor']}")
    print(f"Ano: {data.loc[i, 'ano']}")
    print(f"Preço: {data.loc[i, 'preco_medio']}")
    print()
