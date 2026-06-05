class GramaticaRegular:
    def __init__(self, simbolos_nao_terminais, simbolos_terminais, regras_producao, simbolo_inicial):
        self.simbolos_nao_terminais = simbolos_nao_terminais
        self.simbolos_terminais = simbolos_terminais
        self.regras_producao = regras_producao
        self.simbolo_inicial = simbolo_inicial

    def formatar_regras(self):
        texto = ""

        for nao_terminal, producoes in self.regras_producao.items():
            producoes_formatadas = " | ".join(producoes)
            texto += f"  {nao_terminal} -> {producoes_formatadas}\n"

        return texto

    def __str__(self):
        return (
            f"Gramática Regular:\n"
            f"Símbolos Não Terminais: {self.simbolos_nao_terminais}\n"
            f"Símbolos Terminais: {self.simbolos_terminais}\n"
            f"Símbolo Inicial: {self.simbolo_inicial}\n"
            f"Regras de Produção:\n"
            f"{self.formatar_regras()}"
        )
    
    def eh_regular(self):
        for nao_terminal, producoes in self.regras_producao.items():
            if nao_terminal not in self.simbolos_nao_terminais:
                return False

            for producao in producoes:
                if producao == "":
                    return False

                if producao == "&":
                    continue

                # Caso A -> a (terminal único)
                if producao in self.simbolos_terminais:
                    continue

                # Caso A -> B (produção unitária / transição épsilon)
                if producao in self.simbolos_nao_terminais:
                    continue

                # Caso A -> aB (terminal seguido de não-terminal)
                # O terminal deve ser o primeiro caractere e o resto um não-terminal válido
                if len(producao) >= 2:
                    terminal = producao[0]
                    nao_terminal_destino = producao[1:]

                    if terminal in self.simbolos_terminais and nao_terminal_destino in self.simbolos_nao_terminais:
                        continue

                return False

        return True