class Automato:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes  # Espera {(estado, simbolo): {conjunto_de_estados}}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def fecho_epsilon(self, estados):
        """Calcula o fecho-épsilon para um conjunto de estados."""
        fecho = set(estados)
        pilha = list(estados)

        while pilha:
            t = pilha.pop()
            # Usamos '&' como representação de épsilon
            if (t, "&") in self.transicoes:
                for proximo in self.transicoes[(t, "&")]:
                    if proximo not in fecho:
                        fecho.add(proximo)
                        pilha.append(proximo)
        return fecho

    def processar_cadeia(self, cadeia):
        """Processa uma cadeia no AFN (suporta AFN com épsilon)."""
        estados_atuais = self.fecho_epsilon({self.estado_inicial})

        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False

            proximos_estados = set()
            for estado in estados_atuais:
                if (estado, simbolo) in self.transicoes:
                    # Garante que lidamos tanto com um único estado quanto com um conjunto
                    destino = self.transicoes[(estado, simbolo)]
                    if isinstance(destino, set):
                        proximos_estados.update(destino)
                    else:
                        proximos_estados.add(destino)

            estados_atuais = self.fecho_epsilon(proximos_estados)

        # Verifica se algum dos estados atuais é um estado final
        return any(estado in self.estados_finais for estado in estados_atuais)
    
    def mostrar(self):
        print("Estados:", self.estados)
        print("Alfabeto:", self.alfabeto)
        print("Estado Inicial:", self.estado_inicial)
        print("Estados Finais:", self.estados_finais)
        print("Transições:")
        for (estado, simbolo), destino in self.transicoes.items():
            print(f"  {estado} --{simbolo}--> {destino}")
