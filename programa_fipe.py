from pulp import *
import pandas as pd

# import da base de dados
data = pd.read_excel('~/Documentos/po_pratica/tabela_nova.xlsx')

# criação das variáveis
carros = data.index.tolist()
tamanho_motor = dict(zip(carros, data['tamanho_motor']))

# definição do problema de otimização
prob = pulp.LpProblem('Maximizar_Potencia', LpMaximize)
escolha = pulp.LpVariable.dicts('Escolha', carros, cat='Binary')

# adiciona a função objetivo
prob += pulp.lpSum([escolha[carro] * tamanho_motor[carro] for carro in carros])

# adicionar restrições
# restrição 1: marca
tipo_marca = 'fiat'
for carro in carros:
    marca = data.loc[carro, 'marca']
    if marca != tipo_marca:
        prob += escolha[carro] == 0

# restrição 2: combustível
tipo_combustivel = 'gasolina'
for carro in carros:
    combustivel = data.loc[carro, 'combustivel']
    if combustivel != tipo_combustivel:
        prob += escolha[carro] == 0

# restrição 3: câmbio
tipo_cambio = 'manual'
for carro in carros:
    cambio = data.loc[carro, 'cambio']
    if cambio != tipo_cambio:
        prob += escolha[carro] == 0

# restrição 4: faixa de preço
preco_maximo = 35000
for carro in carros:
    preco_medio = data.loc[carro, 'preco_medio']
    prob += escolha[carro] <= preco_maximo

# restrição 5: idade máxima do carro
idade_maxima = 8
for carro in carros:
    idade = data.loc[carro, 'idade']
    prob += escolha[carro] <= idade_maxima


# restrição 6: potência máxima ou mínima
tamanho_motor_maximo = 2.0
for carro in carros:
    tamanho_motor = data.loc[carro, 'tamanho_motor']
    prob += escolha[carro] <= tamanho_motor_maximo


# resolver o problema
solver = getSolver('COIN_CMD')
status = prob.solve(solver)

print('Status:', {LpStatus[status]})
# acessar os resultados
carro_selecionado = None
potencia_maxima = 0

for carro in carros:   
    if escolha[carro].varValue == 1:
        carro_selecionado = carro
        potencia_maxima = tamanho_motor[carro]
        break

print('Carro selecionado:', carro_selecionado)
print('Potência máxima:', potencia_maxima)
