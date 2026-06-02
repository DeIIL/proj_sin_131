import sys
from automato import Automato
from gramatica import GramaticaRegular
from conversao_gr_af import gr_para_afn
from conversao_afn_afd import afn_para_afd
from minimizacao_afd import minimizar_afd
from conversao_af_gr import af_para_gr

def exibir_menu_principal():
    print("\n" + "="*40)
    print("          SISTEMA DE AUTÔMATOS")
    print("="*40)
    print("1. Inserir um AFN")
    print("2. Inserir uma Gramática Regular")
    print("0. Sair")
    print("="*40)

def ler_nfa():
    print("\n--- ENTRADA DE AFN ---")
    estados = set(input("Estados (separados por espaço, ex: q0 q1 q2): ").split())
    alfabeto = set(input("Alfabeto (separados por espaço, ex: 0 1): ").split())
    estado_inicial = input("Estado inicial: ")
    estados_finais = set(input("Estados finais (separados por espaço, ex: q1 q2): ").split())
    
    transicoes = {}
    print("\nInsira as transições no formato: origem símbolo destino")
    print("Exemplo: q0 0 q0")
    print("Use '&' para transições épsilon.")
    print("Digite 'fim' para encerrar as transições.")
    
    while True:
        linha = input("> ").strip()
        if linha.lower() == 'fim':
            break
        
        partes = linha.split()
        if len(partes) != 3:
            print("Formato inválido! Use: origem símbolo destino (ex: q0 0 q1)")
            continue
            
        origem, simbolo, destino = partes
        
        if (origem, simbolo) not in transicoes:
            transicoes[(origem, simbolo)] = set()
        
        transicoes[(origem, simbolo)].add(destino)
    
    return Automato(estados, alfabeto, transicoes, estado_inicial, estados_finais)

def ler_gramatica():
    print("\n--- ENTRADA DE GRAMÁTICA REGULAR ---")
    nt = set(input("Símbolos não-terminais (separados por espaço, ex: S A B): ").split())
    t = set(input("Símbolos terminais (separados por espaço, ex: 0 1): ").split())
    inicial = input("Símbolo inicial: ")
    
    regras = {}
    print("\nInsira as regras de produção no formato: A -> producao")
    print("Exemplos: S -> 0A | 1S")
    print("          A -> 0 | &")
    print("Digite 'fim' para encerrar as regras.")
    
    while True:
        linha = input("> ").strip()
        if linha.lower() == 'fim':
            break
            
        if "->" not in linha:
            print("Formato inválido! Use: LADO_ESQUERDO -> PRODUÇÃO")
            continue
            
        esq, dir_part = linha.split("->", 1)
        esq = esq.strip()
        
        producoes = [p.strip() for p in dir_part.split("|")]
        
        if esq not in regras:
            regras[esq] = []
        regras[esq].extend(producoes)
        
    return GramaticaRegular(nt, t, regras, inicial)

def menu_operacoes_afd(afd):
    while True:
        print("\n" + "-"*30)
        print("    OPERAÇÕES COM AFD")
        print("-"*30)
        print("1.2 Simular aceitação de palavras")
        print("1.3 Minimizar o AFD")
        print("1.4 Gerar Gramática Regular equivalente")
        print("0. Voltar ao menu anterior")
        print("-"*30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1.2':
            palavra = input("Digite a palavra para testar (use '' para palavra vazia): ").strip()
            res = afd.processar_cadeia(palavra)
            print(f"\n>>> Resultado: Palavra '{palavra}' foi {'ACEITA' if res else 'REJEITADA'}")
            
        elif opcao == '1.3':
            print("\nMinimizando AFD...")
            afd = minimizar_afd(afd)
            print("\nAFD MINIMIZADO:")
            afd.mostrar()
            
        elif opcao == '1.4':
            print("\nGerando Gramática Regular...")
            gr = af_para_gr(afd)
            print("\nGRAMÁTICA GERADA:")
            print(gr)
            
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def menu_nfa_carregado(afn):
    while True:
        print("\n" + "-"*30)
        print("    OPERAÇÕES COM AFN")
        print("-"*30)
        print("1.1 Converter para AFD")
        print("1.5 Gerar Gramática Regular equivalente")
        print("0. Voltar ao menu principal")
        print("-"*30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1.1':
            print("\nConvertendo AFN para AFD...")
            afd = afn_para_afd(afn)
            print("\nAFD RESULTANTE:")
            afd.mostrar()
            menu_operacoes_afd(afd)
        elif opcao == '1.5':
            print("\nGerando Gramática Regular...")
            gr = af_para_gr(afn)
            print("\nGRAMÁTICA GERADA:")
            print(gr)
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def main():
    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            afn = ler_nfa()
            print("\nAFN CADASTRADO:")
            afn.mostrar()
            menu_nfa_carregado(afn)

        elif opcao == '2':
            gr = ler_gramatica()
            print("\nGRAMÁTICA CADASTRADA:")
            print(gr)
            
            if gr.eh_regular():
                while True:
                    print("\n" + "-"*30)
                    print("    OPERAÇÕES COM GRAMÁTICA")
                    print("-"*30)
                    print("2.1 Gerar AFN equivalente")
                    print("2.2 Gerar AFD equivalente")
                    print("0. Voltar ao menu principal")
                    print("-"*30)
                    
                    sub_opcao = input("Escolha uma opção: ").strip()
                    
                    if sub_opcao == '2.1':
                        afn = gr_para_afn(gr)
                        if afn:
                            print("\nAFN GERADO:")
                            afn.mostrar()
                            menu_nfa_carregado(afn)
                    elif sub_opcao == '2.2':
                        afn = gr_para_afn(gr)
                        if afn:
                            print("\nGerando AFD a partir da gramática...")
                            afd = afn_para_afd(afn)
                            print("\nAFD GERADO:")
                            afd.mostrar()
                            menu_operacoes_afd(afd)
                    elif sub_opcao == '0':
                        break
                    else:
                        print("Opção inválida!")
            else:
                print("\nERRO: A gramática inserida não é regular!")

        elif opcao == '0':
            print("\nEncerrando o programa. Até logo!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
