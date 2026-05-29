from automato import Automato


def adicionar_transicao(transicoes, estado_origem, simbolo, estado_destino):
    if (estado_origem, simbolo) not in transicoes:
        transicoes[(estado_origem, simbolo)] = set()

    transicoes[(estado_origem, simbolo)].add(estado_destino)


def gr_para_afn(gramatica):
    if not gramatica.eh_regular():
        print("A gramática não é regular. Não é possível converter para AFN.")
        return None

    estados = set(gramatica.simbolos_nao_terminais)
    alfabeto = set(gramatica.simbolos_terminais)
    estado_inicial = gramatica.simbolo_inicial
    estados_finais = set()
    transicoes = {}

    estado_final_extra = "FINAL"
    estados.add(estado_final_extra)
    estados_finais.add(estado_final_extra)

    for nao_terminal, producoes in gramatica.regras_producao.items():
        for producao in producoes:

            # Caso 1: produção vazia
            # Exemplo: A -> &
            if producao == "&":
                estados_finais.add(nao_terminal)

            # Caso 2: produção terminal
            # Exemplo: A -> 0
            elif len(producao) == 1:
                simbolo_terminal = producao[0]

                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    simbolo_terminal,
                    estado_final_extra
                )

            # Caso 3: terminal seguido de não terminal
            # Exemplo: A -> 0B
            elif len(producao) == 2:
                simbolo_terminal = producao[0]
                nao_terminal_destino = producao[1]

                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    simbolo_terminal,
                    nao_terminal_destino
                )

    afn = Automato(
        estados,
        alfabeto,
        transicoes,
        estado_inicial,
        estados_finais
    )

    return afn