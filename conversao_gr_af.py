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

    # Gerar um nome de estado para o estado final extra que siga o padrão dos outros
    # Tenta usar letras maiúsculas de A-Z que não estejam em uso
    estado_final_extra = None
    for i in range(ord('A'), ord('Z') + 1):
        letra = chr(i)
        if letra not in estados:
            estado_final_extra = letra
            break
    
    # Se todas as letras de A-Z estiverem em uso, adiciona um sufixo ao símbolo inicial
    if estado_final_extra is None:
        estado_final_extra = gramatica.simbolo_inicial + "*"
        while estado_final_extra in estados:
            estado_final_extra += "*"
    
    estados.add(estado_final_extra)
    estados_finais.add(estado_final_extra)

    for nao_terminal, producoes in gramatica.regras_producao.items():
        for producao in producoes:

            # Caso 1: produção vazia
            # Exemplo: A -> &
            if producao == "&":
                estados_finais.add(nao_terminal)

            # Caso 2: produção de um único não-terminal (transição épsilon)
            # Exemplo: A -> B
            elif producao in gramatica.simbolos_nao_terminais:
                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    "&",
                    producao
                )

            # Caso 3: produção terminal
            # Exemplo: A -> 0
            elif producao in gramatica.simbolos_terminais:
                adicionar_transicao(
                    transicoes,
                    nao_terminal,
                    producao,
                    estado_final_extra
                )

            # Caso 4: terminal seguido de não terminal
            # Exemplo: A -> 0B
            elif len(producao) >= 2:
                simbolo_terminal = producao[0]
                nao_terminal_destino = producao[1:]

                if simbolo_terminal in gramatica.simbolos_terminais and nao_terminal_destino in gramatica.simbolos_nao_terminais:
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