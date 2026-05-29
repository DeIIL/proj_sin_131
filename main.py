from automato import Automato
from gramatica import GramaticaRegular
from conversao_gr_af import gr_para_afn


# ==========================
# TESTE DA GRAMÁTICA REGULAR
# ==========================

gramatica = GramaticaRegular(
    simbolos_nao_terminais={"S", "A"},
    simbolos_terminais={"0", "1"},
    regras_producao={
        "S": ["0A", "1S"],
        "A": ["0S", "1A", "&"]
    },
    simbolo_inicial="S"
)

print("\n===== GRAMÁTICA =====")
print(gramatica)

print("A gramática é regular?", gramatica.eh_regular())


# ==========================
# CONVERSÃO GR -> AFN
# ==========================

afn = gr_para_afn(gramatica)

if afn is not None:
    print("\n===== AFN GERADO A PARTIR DA GRAMÁTICA =====")
    afn.mostrar()


# ==========================
# TESTE DE SIMULAÇÃO DE AFD
# ==========================

estados = {"q0", "q1", "q2"}
alfabeto = {"0", "1"}
inicial = "q0"
finais = {"q2"}

transicoes = {
    ("q0", "0"): "q0",
    ("q0", "1"): "q1",
    ("q1", "0"): "q2",
    ("q1", "1"): "q1",
    ("q2", "0"): "q2",
    ("q2", "1"): "q2"
}

afd = Automato(estados, alfabeto, transicoes, inicial, finais)

print("\n===== AFD DE TESTE =====")
afd.mostrar()

cadeia_usuario = input("\nDigite sua cadeia para testar no AFD: ")

cadeia_valida = True

for simbolo in cadeia_usuario:
    if simbolo not in alfabeto:
        print("A cadeia contém símbolos inválidos.")
        cadeia_valida = False
        break

if cadeia_valida:
    if afd.processar_cadeia(cadeia_usuario):
        print("A cadeia é aceita pelo autômato.")
    else:
        print("A cadeia é rejeitada pelo autômato.")