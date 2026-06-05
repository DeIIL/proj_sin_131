# proj_sin_131
## Instalação

Clone o repositório:

```bash
git clone https://github.com/DeIIL/proj_sin_131.git
cd proj_sin_131
```

Instale as dependências:

```bash
python -m pip install PyQt5 graphviz
```

Também é necessário instalar o Graphviz no sistema e adicionar sua pasta `bin` ao `PATH`.

Para verificar a instalação:

```bash
dot -V
```

## Execução

Para executar a interface gráfica:

```bash
python main_gui.py
```

Para executar pelo terminal:

```bash
python main.py
```

## Formatos de entrada

### Transições do autômato

As transições devem seguir o formato:

```text
origem símbolo destino
```

Exemplo:

```text
q0 0 q1
q0 1 q0
```

O símbolo `&` representa uma transição épsilon.

### Regras de Gramática Regular

As regras devem seguir o formato:

```text
S -> 0A | 1S
A -> 0S | 1A | &
```

O símbolo `&` representa a palavra vazia.

## Limitações

* As entradas devem seguir os formatos definidos;
* A visualização gráfica depende da instalação do Graphviz;
* Os dados não são salvos após o encerramento do programa.
