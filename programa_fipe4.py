import pandas as pd
from pulp import *

# Carregar os dados do arquivo Excel
dados_carros = pd.read_excel('dados_carros.xlsx')

# Criar o problema de maximização
problema = LpProblem("Seleção de Carros", LpMaximize)

# Variáveis de decisão
carros = list(dados_carros.index)
selecionado = LpVariable.dicts("Selecionado", carros, cat='Binary')

# Função objetivo
problema += lpSum(selecionado[carro] * dados_carros.loc[carro, 'tamanho_motor']
                  for carro in carros), "Potência_Total"

# Restrições
combustivel_especifico = 'Diesel'  # Defina o combustível desejado aqui
cambio_especifico = 'manual'  # Defina o tipo de câmbio desejado aqui
faixa_preco_min = 10000  # Defina a faixa de preço mínima aqui
faixa_preco_max = 50000  # Defina a faixa de preço máxima aqui
ano_fabricacao_min = 2015  # Defina o ano de fabricação mínimo aqui
potencia_max = 2.0  # Defina a potência máxima aqui
marca_especifica = ''  # Defina a marca desejada aqui (deixe em branco para buscar todas as marcas)

for carro in carros:
    # Restrição de combustível
    if dados_carros.loc[carro, 'combustivel'] != combustivel_especifico and combustivel_especifico != 'Qualquer':
        problema += selecionado[carro] == 0

    # Restrição de câmbio
    if dados_carros.loc[carro, 'cambio'] != cambio_especifico and cambio_especifico != 'Ambos':
        problema += selecionado[carro] == 0

    # Restrição de faixa de preço
    if dados_carros.loc[carro, 'preco_medio'] < faixa_preco_min or dados_carros.loc[carro, 'preco_medio'] > faixa_preco_max:
        problema += selecionado[carro] == 0

    # Restrição de ano de fabricação
    if dados_carros.loc[carro, 'ano'] < ano_fabricacao_min:
        problema += selecionado[carro] == 0

    # Restrição de potência
    if dados_carros.loc[carro, 'tamanho_motor'] > potencia_max:
        problema += selecionado[carro] == 0

    # Restrição de marca
    if marca_especifica != '' and dados_carros.loc[carro, 'marca'] != marca_especifica:
        problema += selecionado[carro] == 0

# Restrição de modelos diferentes com o mesmo nome
modelos_selecionados = []
for carro in carros:
    modelo = dados_carros.loc[carro, 'modelo']
    if modelo in modelos_selecionados:
        problema += selecionado[carro] == 0
    else:
        modelos_selecionados.append(modelo)

# Resolver o problema
problema.solve()

# Extrair os resultados
resultados = []
for carro in carros:
    if selecionado[carro].varValue == 1:
        resultados.append(carro)

# Mostrar os 5 melhores carros selecionados
print("Os 5 melhores carros:")
for i, carro in enumerate(resultados[:5]):
    print(f"{i+1}. {dados_carros.loc[carro, 'marca']} {dados_carros.loc[carro, 'modelo']}, Potência: {dados_carros.loc[carro, 'tamanho_motor']}, Preço Médio: {dados_carros.loc[carro, 'preco_medio']}")
