import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QTextEdit, QMessageBox, QTextBrowser, 
    QInputDialog, QScrollArea, QStackedWidget, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# Importações do seu backend
from automato import Automato
from gramatica import GramaticaRegular
from conversao_gr_af import gr_para_afn
from conversao_afn_afd import afn_para_afd
from minimizacao_afd import minimizar_afd
from conversao_af_gr import af_para_gr

# Tenta importar o graphviz
try:
    import graphviz
    GRAPHVIZ_DISPONIVEL = True
except ImportError:
    GRAPHVIZ_DISPONIVEL = False


def formatar_automato(automato):
    """Função auxiliar para formatar os dados do autômato em texto."""
    texto = f"📌 ESTADOS: {', '.join(sorted(automato.estados))}\n"
    texto += f"🔤 ALFABETO: {', '.join(sorted(automato.alfabeto))}\n"
    texto += f"🏁 ESTADO INICIAL: {automato.estado_inicial}\n"
    texto += f"🎯 ESTADOS FINAIS: {', '.join(sorted(automato.estados_finais))}\n"
    texto += "\n🔄 TRANSIÇÕES:\n"
    for (estado, simbolo), destino in automato.transicoes.items():
        dst = ", ".join(destino) if isinstance(destino, set) else destino
        texto += f"  {estado} --({simbolo})--> {dst}\n"
    return texto


class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.objeto_atual = None
        self.tipo_atual = None  # "AFN", "AFD" ou "GR"
        
        self.setWindowTitle("Sistema de Autômatos Finitos e Gramáticas")
        self.setGeometry(100, 100, 1100, 700) # Janela ampla estilo Dashboard
        
        # Aplicando folha de estilo global (Dark Mode Elegante)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e24;
                color: #e1e1e6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#Sidebar {
                background-color: #121214;
                border-right: 1px solid #29292e;
            }
            QLabel#TituloMenu {
                color: #633bbc;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton {
                background-color: #29292e;
                color: #e1e1e6;
                border: 1px solid #323238;
                border-radius: 6px;
                padding: 10px 15px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #41414c;
                border-color: #633bbc;
            }
            QPushButton:pressed {
                background-color: #633bbc;
            }
            QPushButton#BtnAcaoPrincipal {
                background-color: #8257e5;
                color: white;
                text-align: center;
            }
            QPushButton#BtnAcaoPrincipal:hover {
                background-color: #9466ff;
            }
            QLineEdit, QTextEdit, QTextBrowser {
                background-color: #121214;
                border: 1px solid #29292e;
                border-radius: 6px;
                padding: 8px;
                color: #e1e1e6;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #8257e5;
            }
            QScrollArea {
                border: 1px solid #29292e;
                background-color: #121214;
            }
        """)
        
        self.initUI()

    def initUI(self):
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # ---------------- MENU LATERAL (SIDEBAR) ----------------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)
        layout_sidebar = QVBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(15, 20, 15, 20)
        layout_sidebar.setSpacing(10)
        
        lbl_menu = QLabel("⚡")
        lbl_menu.setObjectName("TituloMenu")
        lbl_menu.setAlignment(Qt.AlignCenter)
        layout_sidebar.addWidget(lbl_menu)
        
        # Botões de Navegação
        self.btn_nav_afn = QPushButton("📥 Inserir AFN")
        self.btn_nav_gr = QPushButton("📝 Inserir Gramática")
        self.btn_nav_res = QPushButton("⚙️ Operações & Grafo")
        self.btn_nav_res.setEnabled(False) # Só ativa quando houver dados
        
        self.btn_nav_afn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_nav_gr.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_nav_res.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        layout_sidebar.addWidget(self.btn_nav_afn)
        layout_sidebar.addWidget(self.btn_nav_gr)
        layout_sidebar.addWidget(self.btn_nav_res)
        
        layout_sidebar.addStretch()
        
        btn_sair = QPushButton("🚪 Sair do Programa")
        btn_sair.setStyleSheet("background-color: #aa2222; text-align: center;")
        btn_sair.clicked.connect(self.close)
        layout_sidebar.addWidget(btn_sair)
        
        # ---------------- ÁREA CENTRAL (STACKED WIDGET) ----------------
        self.stacked_widget = QStackedWidget()
        
        self.criar_tela_inserir_afn()
        self.criar_tela_inserir_gr()
        self.criar_tela_operacoes_dashboard()
        
        # Adiciona tudo ao layout master
        layout_principal.addWidget(sidebar)
        layout_principal.addWidget(self.stacked_widget)
        self.setLayout(layout_principal)

    # ---- TELA 1: CADASTRO AFN ----
    def criar_tela_inserir_afn(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        layout.addWidget(QLabel("<h2>📥 Cadastrar Novo AFN</h2>"))
        
        self.input_estados = QLineEdit()
        self.input_estados.setPlaceholderText("Ex: q0 q1 q2")
        self.input_alfabeto = QLineEdit()
        self.input_alfabeto.setPlaceholderText("Ex: 0 1")
        self.input_inicial = QLineEdit()
        self.input_inicial.setPlaceholderText("Ex: q0")
        self.input_finais = QLineEdit()
        self.input_finais.setPlaceholderText("Ex: q2")
        
        self.input_transicoes = QTextEdit()
        self.input_transicoes.setPlaceholderText("Formato: origem símbolo destino\nEx:\nq0 0 q1\nq0 1 q0\nUse & para épsilon transições.")

        layout.addWidget(QLabel("Estados (separados por espaço):"))
        layout.addWidget(self.input_estados)
        layout.addWidget(QLabel("Alfabeto (separados por espaço):"))
        layout.addWidget(self.input_alfabeto)
        layout.addWidget(QLabel("Estado inicial:"))
        layout.addWidget(self.input_inicial)
        layout.addWidget(QLabel("Estados finais (separados por espaço):"))
        layout.addWidget(self.input_finais)
        layout.addWidget(QLabel("Transições da Função de Programa:"))
        layout.addWidget(self.input_transicoes)
        
        btn_criar = QPushButton("Processar e Criar AFN")
        btn_criar.setObjectName("BtnAcaoPrincipal")
        btn_criar.clicked.connect(self.coletar_dados_afn)
        layout.addWidget(btn_criar)
        
        self.stacked_widget.addWidget(page)

    def coletar_dados_afn(self):
        try:
            estados = set(self.input_estados.text().split())
            alfabeto = set(self.input_alfabeto.text().split())
            estado_inicial = self.input_inicial.text().strip()
            estados_finais = set(self.input_finais.text().split())
            
            transicoes = {}
            linhas = self.input_transicoes.toPlainText().strip().split('\n')
            
            for linha in linhas:
                if not linha.strip(): continue
                partes = linha.split()
                if len(partes) != 3:
                    QMessageBox.warning(self, "Erro", f"Formato inválido na linha: {linha}")
                    return
                
                origem, simbolo, destino = partes
                if (origem, simbolo) not in transicoes:
                    transicoes[(origem, simbolo)] = set()
                transicoes[(origem, simbolo)].add(destino)

            afn = Automato(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            self.atualizar_dashboard_resultados(afn, "AFN")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar o Autômato:\n{str(e)}")

    # ---- TELA 2: CADASTRO GRAMÁTICA ----
    def criar_tela_inserir_gr(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        layout.addWidget(QLabel("<h2>📝 Cadastrar Nova Gramática Regular</h2>"))
        
        self.input_nt = QLineEdit()
        self.input_nt.setPlaceholderText("Ex: S A B")
        self.input_t = QLineEdit()
        self.input_t.setPlaceholderText("Ex: a b")
        self.input_gr_inicial = QLineEdit()
        self.input_gr_inicial.setPlaceholderText("Ex: S")
        
        self.input_regras = QTextEdit()
        self.input_regras.setPlaceholderText("Formato: S -> aA | bS | &")

        layout.addWidget(QLabel("Símbolos Não-terminais (separados por espaço):"))
        layout.addWidget(self.input_nt)
        layout.addWidget(QLabel("Símbolos Terminais (separados por espaço):"))
        layout.addWidget(self.input_t)
        layout.addWidget(QLabel("Símbolo inicial:"))
        layout.addWidget(self.input_gr_inicial)
        layout.addWidget(QLabel("Regras de Produção:"))
        layout.addWidget(self.input_regras)
        
        btn_criar = QPushButton("Processar e Criar Gramática")
        btn_criar.setObjectName("BtnAcaoPrincipal")
        btn_criar.clicked.connect(self.coletar_dados_gr)
        layout.addWidget(btn_criar)
        
        self.stacked_widget.addWidget(page)

    def coletar_dados_gr(self):
        try:
            nt = set(self.input_nt.text().split())
            t = set(self.input_t.text().split())
            inicial = self.input_gr_inicial.text().strip()
            regras = {}

            linhas = self.input_regras.toPlainText().strip().split('\n')
            for linha in linhas:
                if not linha.strip(): continue
                if "->" not in linha:
                    QMessageBox.warning(self, "Erro", f"Formato inválido na linha: {linha}")
                    return
                
                esq, dir_part = linha.split("->", 1)
                esq = esq.strip()
                producoes = [p.strip() for p in dir_part.split("|")]
                
                if esq not in regras:
                    regras[esq] = []
                regras[esq].extend(producoes)

            gr = GramaticaRegular(nt, t, regras, inicial)
            self.atualizar_dashboard_resultados(gr, "GR")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar a Gramática:\n{str(e)}")

    # ---- TELA 3: PAINEL DE OPERAÇÕES INTEGRADO (O SEGREDÃO) ----
    def criar_tela_operacoes_dashboard(self):
        page = QWidget()
        layout_master = QVBoxLayout(page)
        layout_master.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_status_dashboard = QLabel("<h2>⚙️ Operações e Visualização Avançada</h2>")
        layout_master.addWidget(self.lbl_status_dashboard)
        
        # Divisão horizontal: Esquerda (Ações/Texto), Direita (Grafo)
        painel_conteudo = QHBoxLayout()
        
        # LADO ESQUERDO: Dados textuais e botões de cálculo
        coluna_esquerda = QVBoxLayout()
        self.txt_display_dados = QTextBrowser()
        self.txt_display_dados.setFont(QFont("Consolas", 11))
        self.txt_display_dados.setFixedWidth(350)
        coluna_esquerda.addWidget(self.txt_display_dados)
        
        # Container de botões operacionais dinâmicos
        self.layout_botoes_op = QVBoxLayout()
        
        self.btn_op_afd = QPushButton("⚡ Converter para AFD")
        self.btn_op_simular = QPushButton("🎯 Simular Palavra")
        self.btn_op_minimizar = QPushButton("📉 Minimizar AFD")
        self.btn_op_gr = QPushButton("📝 Gerar Gramática Regular")
        self.btn_op_afn = QPushButton("⚙️ Gerar AFN da Gramática")
        self.btn_op_afd_de_gr = QPushButton("🚀 Gerar AFD Direto da GR")
        
        # Conectando ações das operações internas
        self.btn_op_afd.clicked.connect(lambda: self.atualizar_dashboard_resultados(afn_para_afd(self.objeto_atual), "AFD"))
        self.btn_op_minimizar.clicked.connect(lambda: self.atualizar_dashboard_resultados(minimizar_afd(self.objeto_atual), "AFD"))
        self.btn_op_gr.clicked.connect(lambda: self.atualizar_dashboard_resultados(af_para_gr(self.objeto_atual), "GR"))
        self.btn_op_simular.clicked.connect(self.operacao_simular_palavra)
        self.btn_op_afn.clicked.connect(self.operacao_gr_para_afn)
        self.btn_op_afd_de_gr.clicked.connect(self.operacao_gr_para_afd)
        
        self.layout_botoes_op.addWidget(self.btn_op_afd)
        self.layout_botoes_op.addWidget(self.btn_op_simular)
        self.layout_botoes_op.addWidget(self.btn_op_minimizar)
        self.layout_botoes_op.addWidget(self.btn_op_gr)
        self.layout_botoes_op.addWidget(self.btn_op_afn)
        self.layout_botoes_op.addWidget(self.btn_op_afd_de_gr)
        
        coluna_esquerda.addLayout(self.layout_botoes_op)
        painel_conteudo.addLayout(coluna_esquerda)
        
        # LADO DIREITO: Exibição interna do Grafo Renderizado
        coluna_direita = QVBoxLayout()
        
        self.btn_desenhar_grafo = QPushButton("🎨 Renderizar e Exibir Grafo Visual")
        self.btn_desenhar_grafo.setObjectName("BtnAcaoPrincipal")
        self.btn_desenhar_grafo.clicked.connect(self.renderizar_grafo_na_tela)
        coluna_direita.addWidget(self.btn_desenhar_grafo)
        
        # Área de Scroll interna para o desenho
        self.scroll_grafo = QScrollArea()
        self.scroll_grafo.setWidgetResizable(True)
        self.lbl_canvas_grafo = QLabel("O grafo renderizado aparecerá aqui.")
        self.lbl_canvas_grafo.setAlignment(Qt.AlignCenter)
        self.lbl_canvas_grafo.setStyleSheet("background-color: #121214; color: #7c7c8a;")
        self.scroll_grafo.setWidget(self.lbl_canvas_grafo)
        
        coluna_direita.addWidget(self.scroll_grafo)
        painel_conteudo.addLayout(coluna_direita)
        
        layout_master.addLayout(painel_conteudo)
        self.stacked_widget.addWidget(page)

    # ---- CONTROLADOR CENTRAL DA INTERFACE (Muda as telas e dados) ----
    def atualizar_dashboard_resultados(self, objeto, tipo):
        self.objeto_atual = objeto
        self.tipo_atual = tipo
        
        # Altera o título da área ativa
        self.lbl_status_dashboard.setText(f"<h2>⚙️ Operações e Visualização - Estrutura Atual: [{tipo}]</h2>")
        
        # Atualiza o campo de texto estrutural
        if tipo in ["AFN", "AFD"]:
            self.txt_display_dados.setText(formatar_automato(objeto))
            self.btn_desenhar_grafo.setEnabled(True)
            self.btn_desenhar_grafo.setText("🎨 Renderizar e Exibir Grafo Visual")
        else:
            self.txt_display_dados.setText(str(objeto))
            self.btn_desenhar_grafo.setEnabled(False)
            self.btn_desenhar_grafo.setText("🚫 Grafos indisponíveis para Gramáticas")
            
        # Reseta o painel de imagens interno
        self.lbl_canvas_grafo.clear()
        self.lbl_canvas_grafo.setText("O modelo estrutural mudou. Clique no botão acima para renderizar o novo grafo.")
        
        # Esconde TODOS os botões operacionais primeiro
        self.btn_op_afd.hide()
        self.btn_op_simular.hide()
        self.btn_op_minimizar.hide()
        self.btn_op_gr.hide()
        self.btn_op_afn.hide()
        self.btn_op_afd_de_gr.hide()
        
        # Exibe apenas os botões válidos para o tipo de dado atual
        if tipo == "AFN":
            self.btn_op_afd.show()
            self.btn_op_gr.show()
        elif tipo == "AFD":
            self.btn_op_simular.show()
            self.btn_op_minimizar.show()
            self.btn_op_gr.show()
        elif tipo == "GR":
            self.btn_op_afn.show()
            self.btn_op_afd_de_gr.show()
            
        # Libera o menu de resultados e salta para a tela de operações automaticamente
        self.btn_nav_res.setEnabled(True)
        self.stacked_widget.setCurrentIndex(2)

    # ---- MÉTODOS DE CÁLCULO DO BACKEND ----
    def operacao_simular_palavra(self):
        palavra, ok = QInputDialog.getText(self, "Simulador", "Insira a cadeia de teste:")
        if ok:
            res = self.objeto_atual.processar_cadeia(palavra.strip())
            status = "ACEITA 🎉" if res else "REJEITADA ❌"
            QMessageBox.information(self, "Resultado da Cadeia", f"A palavra '{palavra}' foi {status}.")

    def operacao_gr_para_afn(self):
        afn = gr_para_afn(self.objeto_atual)
        if afn: self.atualizar_dashboard_resultados(afn, "AFN")
        else: QMessageBox.warning(self, "Erro", "A gramática informada viola as regras de regularidade.")

    def operacao_gr_para_afd(self):
        afn = gr_para_afn(self.objeto_atual)
        if afn: self.atualizar_dashboard_resultados(afn_para_afd(afn), "AFD")
        else: QMessageBox.warning(self, "Erro", "A gramática informada não é regular.")

    # ---- LÓGICA RENDERIZADORA DO GRAPHVIZ INTEGRADO ----
    def renderizar_grafo_na_tela(self):
        if not GRAPHVIZ_DISPONIVEL:
            QMessageBox.critical(self, "Erro", "Instale a ponte do python: pip install graphviz")
            return
        
        try:
            dot = graphviz.Digraph(
                comment='Automato', 
                graph_attr={
                    'rankdir': 'LR', 'splines': 'true', 
                    'nodesep': '0.6', 'ranksep': '0.8', 'bgcolor': '#121214' # Fundo igual ao da interface!
                },
                node_attr={
                    'fontname': 'Segoe UI', 'fontsize': '12', 'fontcolor': '#ffffff',
                    'style': 'filled', 'fillcolor': '#202024', 'color': '#8257e5',
                    'penwidth': '2', 'fixedsize': 'false', 'width': '0.6', 'height': '0.6'
                },
                edge_attr={
                    'fontname': 'Segoe UI', 'fontsize': '11', 'fontcolor': '#9466ff',
                    'color': '#41414c', 'arrowsize': '0.8', 'penwidth': '1.5'
                }
            )
            
            dot.node('start', shape='point', width='0.05', color='#8257e5')
            
            for estado in self.objeto_atual.estados:
                if estado in self.objeto_atual.estados_finais:
                    dot.node(estado, shape='doublecircle', fillcolor='#122918', color='#04d361')
                else:
                    dot.node(estado, shape='circle')
            
            dot.edge('start', self.objeto_atual.estado_inicial, color='#8257e5', penwidth='2')
            
            arestas = {}
            for (origem, simbolo), destinos in self.objeto_atual.transicoes.items():
                lista_destinos = destinos if isinstance(destinos, set) else {destinos}
                for destino in lista_destinos:
                    chave = (origem, destino)
                    if chave not in arestas: arestas[chave] = []
                    arestas[chave].append(simbolo)
            
            for (origem, destino), simbolos in arestas.items():
                rotulo = " " + ", ".join(sorted(simbolos)) + " "
                dot.edge(origem, destino, label=rotulo)
            
            nome_arquivo = "dashboard_automato"
            caminho_imagem = dot.render(nome_arquivo, format='png', cleanup=True)
            
            # Carrega a imagem direto na tela atual!
            pixmap = QPixmap(caminho_imagem)
            self.lbl_canvas_grafo.setPixmap(pixmap)
            
            # Deleta o arquivo físico pois ele já está salvo no buffer de memória da tela
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                
        except graphviz.backend.execute.ExecutableNotFound:
            QMessageBox.critical(self, "Graphviz Faltando", "Instale o binário do Graphviz no Windows e configure o PATH do sistema.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na renderização:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())