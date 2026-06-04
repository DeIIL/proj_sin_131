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

                # Caso 1: Produção de um único símbolo (terminal ou não-terminal)
                # Exemplo: A -> a ou A -> B
                if producao in self.simbolos_terminais or producao in self.simbolos_nao_terminais:
                    continue

                # Caso 2: Produção terminal seguido de não-terminal
                # Exemplo: A -> aB
                elif len(producao) >= 2:
                    terminal = producao[0]
                    nao_terminal_destino = producao[1:]

                    if terminal in self.simbolos_terminais and nao_terminal_destino in self.simbolos_nao_terminais:
                        continue
                    else:
                        return False

                else:
                    return False

        return True