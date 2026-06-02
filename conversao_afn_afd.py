from automato import Automato

def afn_para_afd(afn):
    """
    Converte um AFN (que pode ter transições épsilon) em um AFD equivalente
    usando o algoritmo de construção de subconjuntos.
    """
    alfabeto = afn.alfabeto
    
    # O estado inicial do AFD é o fecho-épsilon do estado inicial do AFN
    estado_inicial_afn_fecho = tuple(sorted(list(afn.fecho_epsilon({afn.estado_inicial}))))
    
    # Mapeamento de conjunto de estados (como tupla ordenada) para o nome do estado no AFD
    # Exemplo: ('A', 'S') -> "A,S"
    conjuntos_para_nome = {estado_inicial_afn_fecho: ",".join(estado_inicial_afn_fecho) if estado_inicial_afn_fecho else "VAZIO"}
    
    novos_estados = [estado_inicial_afn_fecho]
    processados = []
    
    transicoes_afd = {}
    estados_finais_afd = set()
    
    while novos_estados:
        conjunto_atual = novos_estados.pop(0)
        processados.append(conjunto_atual)
        
        nome_origem = conjuntos_para_nome[conjunto_atual]
        
        # Verifica se é estado final (se contém algum estado final do AFN)
        if any(est in afn.estados_finais for est in conjunto_atual):
            estados_finais_afd.add(nome_origem)
            
        for simbolo in alfabeto:
            # Encontrar para onde o conjunto atual vai com este símbolo
            proximos_afn = set()
            for est in conjunto_atual:
                if (est, simbolo) in afn.transicoes:
                    destino = afn.transicoes[(est, simbolo)]
                    if isinstance(destino, set):
                        proximos_afn.update(destino)
                    else:
                        proximos_afn.add(destino)
            
            # Aplica o fecho épsilon nos destinos
            fecho_destinos = tuple(sorted(list(afn.fecho_epsilon(proximos_afn))))
            
            if not fecho_destinos:
                continue # Caminho morto no AFD (ou podemos criar um estado de erro/lixo)
            
            if fecho_destinos not in conjuntos_para_nome:
                nome_novo = ",".join(fecho_destinos)
                conjuntos_para_nome[fecho_destinos] = nome_novo
                novos_estados.append(fecho_destinos)
            
            nome_destino = conjuntos_para_nome[fecho_destinos]
            transicoes_afd[(nome_origem, simbolo)] = nome_destino
            
    return Automato(
        estados=set(conjuntos_para_nome.values()),
        alfabeto=alfabeto,
        transicoes=transicoes_afd,
        estado_inicial=conjuntos_para_nome[estado_inicial_afn_fecho],
        estados_finais=estados_finais_afd
    )
