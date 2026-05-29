class Automato:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def processar_cadeia(self, cadeia):
        estado_atual = self.estado_inicial

        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False  # Símbolo não pertence ao alfabeto

            if (estado_atual, simbolo) not in self.transicoes:
                return False  # Transição não definida para o estado atual e símbolo

            estado_atual = self.transicoes[(estado_atual, simbolo)]

        return estado_atual in self.estados_finais  # Verifica se o estado final é alcançado
    
    def mostrar(self):
        print("Estados:", self.estados)
        print("Alfabeto:", self.alfabeto)
        print("Estado Inicial:", self.estado_inicial)
        print("Estados Finais:", self.estados_finais)
        print("Transições:")
        for (estado, simbolo), proximo_estado in self.transicoes.items():
            print(f"  {estado} --{simbolo}--> {proximo_estado}")