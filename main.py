from automato import Automato
from gramatica import GramaticaRegular
from conversao_gr_af import gr_para_afn
from conversao_afn_afd import afn_para_afd
from minimizacao_afd import minimizar_afd


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
    # CONVERSÃO AFN -> AFD
    # ==========================
    
    afd_convertido = afn_para_afd(afn)
    
    print("\n===== AFD GERADO A PARTIR DO AFN =====")
    afd_convertido.mostrar()
    print(f"Número de estados do AFD: {len(afd_convertido.estados)}")

    # ==========================
    # MINIMIZAÇÃO DO AFD
    # ==========================
    
    afd_minimizado = minimizar_afd(afd_convertido)
    
    print("\n===== AFD MINIMIZADO =====")
    afd_minimizado.mostrar()
    print(f"Número de estados do AFD Minimizado: {len(afd_minimizado.estados)}")

    print("\n--- Comparando AFN vs AFD Minimizado ---")
    cadeias_teste = ["0", "01", "10", "11", "011", "101", "010"]
    for c in cadeias_teste:
        res_afn = afn.processar_cadeia(c)
        res_afd = afd_minimizado.processar_cadeia(c)
        print(f"Cadeia '{c}': AFN={'OK' if res_afn else 'XX'} | AFD_Min={'OK' if res_afd else 'XX'} -> {'IGUAIS' if res_afn == res_afd else 'ERRO'}")


# ==========================
# TESTE DE AFD (Retrocompatibilidade)
# ==========================

transicoes_afd_manual = {
    ("q0", "0"): "q0",
    ("q0", "1"): "q1",
    ("q1", "0"): "q2",
    ("q1", "1"): "q1",
    ("q2", "0"): "q2",
    ("q2", "1"): "q2"
}

afd_manual = Automato({"q0", "q1", "q2"}, {"0", "1"}, transicoes_afd_manual, "q0", {"q2"})

print("\n===== AFD DE TESTE MANUAL (Exemplo 1*0) =====")
afd_manual.mostrar()
print("Cadeia '010' no AFD Manual:", "Aceita" if afd_manual.processar_cadeia("010") else "Rejeitada")
