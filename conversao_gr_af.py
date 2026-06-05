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

    # Verifica se precisamos de um estado final extra para produções do tipo A -> a
    precisa_final_extra = False
    for producoes in gramatica.regras_producao.values():
        for producao in producoes:
            if len(producao) == 1 and producao != "&":
                precisa_final_extra = True
                break
        if precisa_final_extra:
            break

    estado_final_extra = "Qf"
    if precisa_final_extra:
        # Garante um nome único para o estado final extra
        base_nome = "Qf"
        contador = 1
        while estado_final_extra in estados:
            estado_final_extra = f"{base_nome}_{contador}"
            contador += 1

        estados.add(estado_final_extra)
        estados_finais.add(estado_final_extra)

    for nao_terminal, producoes in gramatica.regras_producao.items():
        for producao in producoes:

            # Caso 1: produção vazia
            # Exemplo: A -> &
            if producao == "&":
                estados_finais.add(nao_terminal)

            # Caso A -> B (transição épsilon / produção unitária)
            elif producao in gramatica.simbolos_nao_terminais:
                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    "&",
                    producao
                )

            # Caso A -> a (produção terminal)
            elif producao in gramatica.simbolos_terminais:
                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    producao,
                    estado_final_extra
                )

            # Caso A -> aB (terminal seguido de não terminal)
            elif len(producao) >= 2 and producao[0] in gramatica.simbolos_terminais:
                simbolo_terminal = producao[0]
                nao_terminal_destino = producao[1:]

                if nao_terminal_destino in gramatica.simbolos_nao_terminais:
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