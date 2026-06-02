from automato import Automato

def remover_estados_inalcancaveis(afd):
    """Remove estados que não podem ser alcançados a partir do estado inicial."""
    alcancaveis = {afd.estado_inicial}
    fila = [afd.estado_inicial]
    
    while fila:
        atual = fila.pop(0)
        for simbolo in afd.alfabeto:
            if (atual, simbolo) in afd.transicoes:
                destino = afd.transicoes[(atual, simbolo)]
                # Lidando com o fato de que transicoes podem ser set (NFA) ou str (DFA)
                destinos = destino if isinstance(destino, set) else {destino}
                for d in destinos:
                    if d not in alcancaveis:
                        alcancaveis.add(d)
                        fila.append(d)
    
    novos_estados = alcancaveis
    novas_transicoes = {
        (e, s): d for (e, s), d in afd.transicoes.items()
        if e in alcancaveis
    }
    novos_estados_finais = afd.estados_finais.intersection(alcancaveis)
    
    return Automato(
        estados=novos_estados,
        alfabeto=afd.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=afd.estado_inicial,
        estados_finais=novos_estados_finais
    )

def minimizar_afd(afd):
    """
    Minimiza um AFD usando o algoritmo de partição (Hopcroft simplificado).
    Assume que o autômato já é um AFD (transições para um único estado).
    """
    # 1. Remover estados inalcançáveis
    afd = remover_estados_inalcancaveis(afd)
    
    estados = list(afd.estados)
    alfabeto = list(afd.alfabeto)
    
    # 2. Partição inicial: estados finais e não-finais
    finais = afd.estados_finais
    nao_finais = afd.estados.difference(finais)
    
    # Representamos partições como tuplas congeladas de estados para facilitar comparação
    particoes = []
    if finais:
        particoes.append(frozenset(finais))
    if nao_finais:
        particoes.append(frozenset(nao_finais))
        
    def get_particao_index(estado, as_particoes):
        for i, p in enumerate(as_particoes):
            if estado in p:
                return i
        return -1 # Para transições "mortas" (opcional se o AFD for completo)

    while True:
        novas_particoes = []
        for p in particoes:
            if len(p) <= 1:
                novas_particoes.append(p)
                continue
            
            # Divide a partição baseada nas transições
            grupos = {}
            for estado in p:
                # Característica do estado: pra qual partição ele vai com cada símbolo
                assinatura = []
                for simbolo in alfabeto:
                    destino = afd.transicoes.get((estado, simbolo))
                    if destino:
                        assinatura.append(get_particao_index(destino, particoes))
                    else:
                        assinatura.append(-1) # Estado de erro/morte
                
                assinatura = tuple(assinatura)
                if assinatura not in grupos:
                    grupos[assinatura] = set()
                grupos[assinatura].add(estado)
            
            for g in grupos.values():
                novas_particoes.append(frozenset(g))
        
        if len(novas_particoes) == len(particoes):
            break
        particoes = novas_particoes

    # 3. Construir o novo AFD a partir das partições
    estado_para_particao_nome = {}
    for p in particoes:
        # Nome da nova partição: concatenação dos nomes dos estados originais
        nome_particao = ",".join(sorted(list(p)))
        for estado in p:
            estado_para_particao_nome[estado] = nome_particao
            
    novos_estados = set(estado_para_particao_nome.values())
    nova_transicoes = {}
    novos_estados_finais = set()
    novo_estado_inicial = estado_para_particao_nome[afd.estado_inicial]
    
    for p in particoes:
        exemplo_estado = next(iter(p))
        nome_origem = estado_para_particao_nome[exemplo_estado]
        
        if exemplo_estado in afd.estados_finais:
            novos_estados_finais.add(nome_origem)
            
        for simbolo in alfabeto:
            destino = afd.transicoes.get((exemplo_estado, simbolo))
            if destino:
                nome_destino = estado_para_particao_nome[destino]
                nova_transicoes[(nome_origem, simbolo)] = nome_destino
                
    return Automato(
        estados=novos_estados,
        alfabeto=set(alfabeto),
        transicoes=nova_transicoes,
        estado_inicial=novo_estado_inicial,
        estados_finais=novos_estados_finais
    )
