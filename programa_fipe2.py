import pandas as pd
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

# carregar os dados do arquivo .xlsx
dados_carros = pd.read_excel('~/Documentos/po_pratica/tabela_nova.xlsx')

# definir as restrições fornecidas pelo usuário
combustivel_restricao = str(input("\n\nEscolha o combustível desejado (Gasolina, Diesel ou Álcool): "))
cambio_restricao = str(input("\nEsolha o câmbio desejado (manual ou automatic): "))
faixa_preco_restricao = [float(input("\nInforme o preço mínimo do carro: ")),
                         float(input("\nInforme o preço máximo: "))]
ano_fabricacao_restricao = int(input("\nInforme o ano mínimo de fabricação: "))
potencia_max_restricao = float(input("\nInforme a potência máxima desejada: "))

# criar o problema de otimização
problema = LpProblem("Otimizacao_Carros", LpMaximize)

# variáveis de decisão
carros = list(dados_carros.index)
x = LpVariable.dicts("carro", carros, lowBound=0, upBound=1, cat='Binary')

# função objetivo
problema += lpSum(dados_carros.loc[carro, 'tamanho_motor'] * x[carro] for carro in carros)

# restrição 1 (combustível)
problema += lpSum(x[carro] for carro in carros
                    if dados_carros.loc[carro, 'combustivel'] != combustivel_restricao) == 0, "Restricao_Combustivel"

# restrição 2 (cambio)
problema += lpSum(x[carro] for carro in carros
                    if dados_carros.loc[carro, 'cambio'] != cambio_restricao) == 0, "Restricao_Cambio"

# restrição 3 (faixa de preço)
problema += lpSum(dados_carros.loc[carro, 'preco_medio'] * x[carro] for carro in carros
                    if dados_carros.loc[carro, 'preco_medio'] < faixa_preco_restricao[0] or
                        dados_carros.loc[carro, 'preco_medio'] > faixa_preco_restricao[1]) == 0

# restrição 4 (ano de fabricação)
problema += lpSum(dados_carros.loc[carro, 'ano'] * x[carro] for carro in carros
                    if dados_carros.loc[carro, 'ano'] < ano_fabricacao_restricao) == 0

# restrição 5 (potência máxima)
problema += lpSum(dados_carros.loc[carro, 'tamanho_motor'] * x[carro] for carro in carros
                    if dados_carros.loc[carro, 'tamanho_motor'] > potencia_max_restricao) == 0

# resolver o problema de otimização
problema.solve()

# verificar o status da solução
status = LpStatus[problema.status]

if status == "Optimal":
    # obter a lista dos carros selecionados
    carros_selecionados = [carro for carro in carros if x[carro].value() == 1]

    # classificar os carros pelo tamanho do motor em ordem decrescente
    carros_selecionados = sorted(carros_selecionados, key=lambda c: dados_carros.loc[c, 'tamanho_motor'], reverse=True)

    # imprimir os 5 melhores carros
    for i, carro in enumerate(carros_selecionados[:5]):
        print(f"Carro {i+1}:")
        print(f"Marca: {dados_carros.loc[carro, 'marca']}")
        print(f"Modelo: {dados_carros.loc[carro, 'modelo']}")
        print(f"Combustivel: {dados_carros.loc[carro, 'combustivel']}")
        print(f"Câmbio: {dados_carros.loc[carro, 'cambio']}")
        print(f"Tamanho do motor: {dados_carros.loc[carro, 'tamanho_motor']}")
        print(f"Ano: {dados_carros.loc[carro, 'ano']}")
        print(f"Preço médio: {dados_carros.loc[carro, 'preco_medio']}")
        print(f"Idade: {dados_carros.loc[carro, 'idade']}")
        print(f"------------------------------")
else:
    print("Não foi possível encontrar uma solução ótima para o problema.")
