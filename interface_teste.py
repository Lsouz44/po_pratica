import curses
import pandas as pd
from pulp import *

# Carregar dados dos carros a partir do arquivo .xlsx
dados_carros = pd.read_excel('dados_carros.xlsx')

# Inicializar a biblioteca curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Função para exibir o menu e obter as restrições do usuário
def exibir_menu():
    stdscr.clear()
    stdscr.addstr("===== MENU =====\n")
    stdscr.addstr("1. Informar tipo de combustível\n")
    stdscr.addstr("2. Informar tipo de câmbio\n")
    stdscr.addstr("3. Informar faixa de preço\n")
    stdscr.addstr("4. Informar ano de fabricação\n")
    stdscr.addstr("5. Informar potência máxima\n")
    stdscr.addstr("6. Executar pesquisa\n")
    stdscr.addstr("================\n")

    stdscr.refresh()

# Função para obter o valor do usuário para uma determinada restrição
def obter_restricao(mensagem):
    stdscr.clear()
    stdscr.addstr(mensagem)
    stdscr.refresh()

    valor = stdscr.getstr().decode("utf-8")
    return valor

# Loop principal
def main(stdscr):
    # Variáveis de decisão
    carros = dados_carros.index
    x = LpVariable.dicts("carro", carros, cat=LpBinary)

    # Variáveis para armazenar as restrições
    combustivel_restricao = ""
    cambio_restricao = ""
    faixa_preco_restricao = []
    ano_fabricacao_restricao = 0
    potencia_max_restricao = 0.0

    while True:
        exibir_menu()
        choice = stdscr.getch()

        if choice == ord('1'):
            combustivel_restricao = obter_restricao("Informe o tipo de combustível (ou 'todos' para considerar todos os tipos): ")
        elif choice == ord('2'):
            cambio_restricao = obter_restricao("Informe o tipo de câmbio: ")
        elif choice == ord('3'):
            faixa_preco_restricao.append(float(obter_restricao("Informe o valor mínimo da faixa de preço: ")))
            faixa_preco_restricao.append(float(obter_restricao("Informe o valor máximo da faixa de preço: ")))
        elif choice == ord('4'):
            ano_fabricacao_restricao = int(obter_restricao("Informe o ano mínimo de fabricação: "))
        elif choice == ord('5'):
            potencia_max_restricao = float(obter_restricao("Informe a potência máxima desejada: "))
        elif choice == ord('6'):
            # Criar a variável do problema
            problema = LpProblem("Selecao_Carros", LpMaximize)

            # Função objetivo
            problema += lpSum(dados_carros.loc[carro, 'tamanho_motor'] * x[carro] for carro in carros), "Funcao_Objetivo"

            # Restrição 1 (combustível)
            if combustivel_restricao == "todos":
                problema += lpSum(x[carro] for carro in carros) == len(carros), "Restricao_Combustivel_Todos"
            else:
                problema += lpSum(x[carro] for carro in carros
                                  if dados_carros.loc[carro, 'combustivel'] != combustivel_restricao) == 0, "Restricao_Combustivel"

            # Restrição 2 (câmbio)
            problema += lpSum(x[carro] for carro in carros
                              if str(dados_carros.loc[carro, 'cambio']) != cambio_restricao) == 0, "Restricao_Cambio"

            # Restrição 3 (faixa de preço)
            problema += lpSum(dados_carros.loc[carro, 'preco_medio'] * x[carro] for carro in carros
                              if faixa_preco_restricao[0] <= dados_carros.loc[carro, 'preco_medio'] <= faixa_preco_restricao[1]), "Restricao_Preco"

            # Restrição 4 (ano de fabricação)
            problema += lpSum(dados_carros.loc[carro, 'ano'] * x[carro] for carro in carros
                              if dados_carros.loc[carro, 'ano'] >= ano_fabricacao_restricao), "Restricao_Ano"

            # Restrição 5 (potência máxima)
            problema += lpSum(dados_carros.loc[carro, 'tamanho_motor'] * x[carro] for carro in carros
                              if dados_carros.loc[carro, 'tamanho_motor'] <= potencia_max_restricao), "Restricao_Potencia"

            # Resolver o problema
            problema.solve()

            # Verificar se foi encontrada uma solução ótima
            if problema.status == LpStatusOptimal:
                # Obter a lista de carros selecionados
                carros_selecionados = [carro for carro in carros if value(x[carro]) == 1]

                # Ordenar os carros pelo valor da função objetivo (potência)
                carros_selecionados.sort(key=lambda carro: dados_carros.loc[carro, 'tamanho_motor'], reverse=True)

                # Exibir os 5 melhores carros
                num_carros_exibidos = min(5, len(carros_selecionados))
                for i in range(num_carros_exibidos):
                    carro = carros_selecionados[i]
                    stdscr.addstr(f"\nCarro {i + 1}:\n")
                    stdscr.addstr(f"Marca: {dados_carros.loc[carro, 'marca']}\n")
                    stdscr.addstr(f"Modelo: {dados_carros.loc[carro, 'modelo']}\n")
                    stdscr.addstr(f"Combustível: {dados_carros.loc[carro, 'combustivel']}\n")
                    stdscr.addstr(f"Câmbio: {dados_carros.loc[carro, 'cambio']}\n")
                    stdscr.addstr(f"Motor: {dados_carros.loc[carro, 'tamanho_motor']}\n")
                    stdscr.addstr(f"Ano: {dados_carros.loc[carro, 'ano']}\n")
                    stdscr.addstr(f"Preço Médio: R${dados_carros.loc[carro, 'preco_medio']}\n")
                    stdscr.addstr(f"Idade: {dados_carros.loc[carro, 'idade']}\n")
                    stdscr.addstr("------------------------------\n")
                stdscr.refresh()
            else:
                stdscr.addstr("Não foi encontrada uma solução ótima.\n")
                stdscr.refresh()

            stdscr.addstr("Pressione qualquer tecla para voltar ao menu.\n")
            stdscr.refresh()
            stdscr.getch()
        elif choice == ord('q'):
            break

# Executar o programa
curses.wrapper(main)

# Restaurar as configurações do terminal
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
