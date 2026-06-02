from gramatica import GramaticaRegular

def af_para_gr(automato):
    """
    Converte um Autômato Finito (AFN ou AFD) em uma Gramática Regular.
    """
    nt = set(automato.estados)
    t = set(automato.alfabeto)
    inicial = automato.estado_inicial
    regras = {}

    for estado in automato.estados:
        regras[estado] = []

    for (origem, simbolo), destinos in automato.transicoes.items():
        # Se for AFN, destinos é um set. Se for AFD, destinos é uma string.
        lista_destinos = destinos if isinstance(destinos, set) else {destinos}
        
        for destino in lista_destinos:
            if simbolo == "&":
                # Transição épsilon: A -> B
                regras[origem].append(destino)
            else:
                # Transição normal: A -> aB
                regras[origem].append(f"{simbolo}{destino}")

    # Adiciona produções vazias para estados finais: A -> &
    for estado_final in automato.estados_finais:
        if estado_final in regras:
            regras[estado_final].append("&")
        else:
            regras[estado_final] = ["&"]

    return GramaticaRegular(nt, t, regras, inicial)
