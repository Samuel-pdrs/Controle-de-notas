# -*- coding: utf-8 -*-
"""
SISTEMA DE CONTROLE DE NOTAS - UNIDADE CARANGOLA UEMG
Sistemas de Informação - 2º Período
Algoritmos e Programação - Paradigma Procedural Estruturado

Este programa foi desenvolvido seguindo estritamente as diretrizes pedagógicas de
programação procedural/estruturada pura (sem uso de classes), organizando o fluxo principal
em Sequência, Seleção e Repetição (Estruturas de Böhm-Jacopini).
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ==============================================================================
# DECLARAÇÃO DE VARIÁVEIS GLOBAIS (ESTRUTURAS DE DADOS)
# ==============================================================================
# Vetor unidimensional para armazenar os nomes dos 5 alunos
# Inicializado com strings vazias.
vetor_nomes = [""] * 5

# Matriz bidimensional (5 linhas por 3 colunas) para armazenar as notas de cada aluno
# Cada linha correspondente ao aluno do mesmo índice do vetor.
# Inicializada com valores reais (float) zerados.
matriz_notas = [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]
]

# Listas globais para armazenar as referências dos componentes visuais (Widgets Entry)
# que permitirão coletar os dados inseridos pelo usuário.
widget_entradas_nomes = []  # Armazenará as referências dos 5 campos de texto dos nomes
widget_entradas_notas = []  # Armazenará 5 listas (uma por aluno), contendo 3 referências de campos de nota cada


# ==============================================================================
# FUNÇÕES DE REGRA DE NEGÓCIO E LÓGICA DO SISTEMA (PROCEDURAL)
# ==============================================================================

def validar_e_coletar_dados():
    """
    Função de validação e coleta de dados (Sequência, Repetição e Seleção).
    Lê os dados da interface gráfica, valida se o nome está preenchido e se as
    notas estão no intervalo de [0.0, 10.0]. Atualiza o vetor de nomes e a matriz de notas.
    Retorna True se todos os dados forem válidos, caso contrário, exibe um erro e retorna False.
    """
    # [REPETIÇÃO] Estrutura de iteração controlada (for loop)
    # Explicação pedagógica: Percorre cada um dos 5 índices de alunos para validar e coletar dados individuais.
    # Em termos de algoritmo tradicional, equivale a um loop iterativo "De i = 0 Até 4".
    for i in range(5):
        # Coleta o nome inserido e remove espaços em branco extras
        # [MÉTODO NATIVO: strip()]
        # "strip()" é um método utilitário que remove espaços em branco antes e depois da string.
        # Por debaixo dos panos, ele percorre a string, identifica os caracteres invisíveis nas extremidades e
        # fatia a string correspondente. Substitui um loop manual de busca por caracteres não-espaço.
        nome = widget_entradas_nomes[i].get().strip()
        
        # [SELEÇÃO] Estrutura de decisão para verificar se o campo nome foi preenchido
        if nome == "":
            messagebox.showerror(
                "Erro de Validação", 
                f"Por favor, insira o nome do Aluno {i+1} antes de calcular."
            )
            return False
        
        # Armazena o nome no vetor correspondente (Regra de Negócio: DADO que existam alunos a serem registrados...)
        vetor_nomes[i] = nome
        
        # [REPETIÇÃO] Percorre as 3 notas do aluno atual (Matriz de 5x3)
        # Em termos algorítmicos, esta estrutura aninhada representa o preenchimento de uma matriz bidimensional.
        for j in range(3):
            nota_str = widget_entradas_notas[i][j].get().strip()
            
            # [SELEÇÃO] Verifica se a nota está vazia
            if nota_str == "":
                messagebox.showerror(
                    "Erro de Validação", 
                    f"A Nota {j+1} do Aluno '{nome}' está vazia. Preencha todos os campos."
                )
                return False
            
            # Tratamento de exceção para conversão do valor para float (dados numéricos inconsistentes)
            try:
                # Converte o texto em número de ponto flutuante
                nota_val = float(nota_str.replace(",", ".")) # Permite o uso de vírgula como separador decimal
            except ValueError:
                messagebox.showerror(
                    "Erro de Formato", 
                    f"A Nota {j+1} do Aluno '{nome}' contém caracteres inválidos.\nInsira apenas números de 0 a 10."
                )
                return False
            
            # [SELEÇÃO] Validação dos limites regulamentares (Notas de 0 a 10)
            if nota_val < 0.0 or nota_val > 10.0:
                messagebox.showerror(
                    "Erro de Limite", 
                    f"A Nota {j+1} do Aluno '{nome}' é {nota_val}.\nAs notas aceitas devem estar estritamente entre 0.0 e 10.0."
                )
                return False
            
            # Armazena na matriz de notas (Regra de Negócio: DADO que um aluno esteja identificado no vetor...)
            matriz_notas[i][j] = nota_val
            
    return True


def calcular_resultados():
    """
    Função principal de processamento dos resultados (Sequência, Seleção e Repetição).
    Acionada pelo botão 'Calcular Resultados'.
    Calcula a soma, média e situação de cada aluno, exibe na tabela e gera as estatísticas da turma.
    """
    # 1. Validação prévia
    if not validar_e_coletar_dados():
        return  # Interrompe a execução caso os dados estejam inconsistentes
        
    # Limpa as exibições anteriores da tabela de resultados
    for item in tree_resultados.get_children():
        tree_resultados.delete(item)
        
    # Inicializa variáveis para as estatísticas gerais da turma
    soma_medias_turma = 0.0
    total_aprovados = 0
    total_reprovados = 0
    lista_medias = []  # Vetor auxiliar para encontrar a maior e menor média com facilidade
    
    # [REPETIÇÃO] Percorre o vetor de alunos e matriz de notas para calcular os resultados individuais
    for i in range(5):
        aluno = vetor_nomes[i]
        notas_aluno = matriz_notas[i]  # Fatiamento/Referência de linha da matriz
        
        # [FUNÇÃO NATIVA: sum()]
        # "sum(iterable)" soma todos os elementos numéricos do iterável.
        # Por debaixo dos panos, o interpretador Python realiza um loop de acumulação manual,
        # inicializando uma variável acumuladora em zero e iterando por todos os elementos da lista, somando-os.
        # Algoritmo equivalente:
        #   soma_acumulada = 0
        #   for nota in notas_aluno:
        #       soma_acumulada += nota
        soma_notas = sum(notas_aluno)
        
        # [FUNÇÃO NATIVA: len()]
        # "len(iterable)" retorna a quantidade de itens no iterável.
        # Por debaixo dos panos, retorna diretamente o atributo de tamanho pré-armazenado no objeto lista (O(1)).
        # Substitui a contagem manual via loop de incremento unitário.
        media = soma_notas / len(notas_aluno)
        
        # [SELEÇÃO] Define a situação com base na média calculada
        # Regra de Negócio: Média >= 6.0 (Aprovado), Média < 6.0 (Reprovado)
        if media >= 6.0:
            situacao = "Aprovado"
            total_aprovados += 1
        else:
            situacao = "Reprovado"
            total_reprovados += 1
            
        # Acumula a média para posterior cálculo da média da turma
        soma_medias_turma += media
        # Guarda na lista de médias para facilitar os cálculos estatísticos de extremos (maior/menor)
        lista_medias.append(media)
        
        # Insere os resultados individuais na Treeview gráfica
        tree_resultados.insert(
            "", 
            "end", 
            values=(
                aluno, 
                f"{notas_aluno[0]:.1f}", 
                f"{notas_aluno[1]:.1f}", 
                f"{notas_aluno[2]:.1f}", 
                f"{media:.2f}", 
                situacao
            ),
            tags=(situacao.lower(),)  # Permite estilizar a linha baseando-se na situação
        )

    # 2. Estatísticas Gerais da Turma (Cálculos de Extremos e Média Geral)
    # [FUNÇÃO NATIVA: len()]
    # Obtém o total de alunos na lista (neste caso, fixado em 5).
    total_alunos = len(lista_medias)
    
    # Calcula a média geral da turma
    media_geral_turma = soma_medias_turma / total_alunos if total_alunos > 0 else 0.0
    
    # [FUNÇÃO NATIVA: max()]
    # "max(iterable)" retorna o maior valor dentro do iterável.
    # Por debaixo dos panos, assume o primeiro elemento como o maior temporário, percorre o restante do vetor
    # usando uma estrutura condicional de seleção (if item > maior_temporario) e atualiza-o quando necessário.
    # Algoritmo equivalente:
    #   maior_temporario = lista_medias[0]
    #   for m in lista_medias:
    #       if m > maior_temporario:
    #           maior_temporario = m
    maior_media = max(lista_medias)
    
    # [FUNÇÃO NATIVA: min()]
    # "min(iterable)" retorna o menor valor dentro do iterável.
    # Por debaixo dos panos, executa uma lógica de busca linear análoga à do max(),
    # utilizando a condição de seleção de menor elemento (if item < menor_temporario).
    # Algoritmo equivalente:
    #   menor_temporario = lista_medias[0]
    #   for m in lista_medias:
    #       if m < menor_temporario:
    #           menor_temporario = m
    menor_media = min(lista_medias)
    
    # Atualiza as labels de resumo geral na interface do Windows com os dados calculados
    lbl_media_turma_val.config(text=f"{media_geral_turma:.2f}")
    lbl_aprovados_val.config(text=f"{total_aprovados} ({ (total_aprovados/total_alunos)*100:.1f}%)")
    lbl_reprovados_val.config(text=f"{total_reprovados} ({ (total_reprovados/total_alunos)*100:.1f}%)")
    lbl_maior_media_val.config(text=f"{maior_media:.2f}")
    lbl_menor_media_val.config(text=f"{menor_media:.2f}")
    
    # Aplica configurações visuais para destacar aprovados em verde e reprovados em vermelho
    tree_resultados.tag_configure("aprovado", foreground="#1b5e20", font=("Segoe UI", 9, "bold"))
    tree_resultados.tag_configure("reprovado", foreground="#b71c1c", font=("Segoe UI", 9, "bold"))
    
    # Notificação de sucesso ao usuário
    messagebox.showinfo("Sucesso", "Resultados e Estatísticas calculados com sucesso!")


def limpar_dados():
    """
    Função para reiniciar os dados do programa (Sequência e Repetição).
    Limpa as entradas de texto, reinicializa as estruturas de dados globais (vetor e matriz)
    e restaura as etiquetas de resumo para o estado inicial.
    """
    # Confirmação de segurança para evitar exclusão acidental
    decisao = messagebox.askyesno("Limpar Dados", "Deseja realmente apagar todos os dados e reiniciar o sistema?")
    if not decisao:
        return
        
    # [REPETIÇÃO] Reseta o vetor e a matriz globais, e limpa os campos de texto na tela.
    for i in range(5):
        vetor_nomes[i] = ""
        widget_entradas_nomes[i].delete(0, tk.END)
        for j in range(3):
            matriz_notas[i][j] = 0.0
            widget_entradas_notas[i][j].delete(0, tk.END)
            
    # Limpa a tabela de resultados individuais
    for item in tree_resultados.get_children():
        tree_resultados.delete(item)
        
    # Restaura as etiquetas estatísticas
    lbl_media_turma_val.config(text="-")
    lbl_aprovados_val.config(text="-")
    lbl_reprovados_val.config(text="-")
    lbl_maior_media_val.config(text="-")
    lbl_menor_media_val.config(text="-")
    
    # Posiciona o foco do teclado de volta no primeiro campo de nome
    widget_entradas_nomes[0].focus_set()
    
    messagebox.showinfo("Limpeza", "Todos os dados foram resetados com sucesso!")


# ==============================================================================
# CONSTRUÇÃO DA INTERFACE GRÁFICA (WINDOWS STYLE COM TKINTER/TTK)
# ==============================================================================

# Criação da janela principal da aplicação
root = tk.Tk()
root.title("Sistema de Controle de Notas - UEMG Carangola")
root.geometry("820x680")
root.resizable(False, False)

# Configuração de Cores e Estilo Visual Nativo do Windows
style = ttk.Style()
# Define o tema "vista" ou "xpnative" caso disponíveis, ou o padrão para uma aparência Windows moderna
style.theme_use('vista' if 'vista' in style.theme_names() else 'clam')

# Customização do design de botões e tabelas
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1e3d59")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)

# [SEQUÊNCIA] Organização das seções da janela em frames hierárquicos de cima para baixo.

# 1. Cabeçalho Principal (Título Acadêmico)
frame_cabecalho = ttk.Frame(root, padding=10)
frame_cabecalho.pack(fill=tk.X)

lbl_titulo = ttk.Label(
    frame_cabecalho, 
    text="SISTEMA DE CONTROLE DE NOTAS - UEMG CARANGOLA", 
    style="Title.TLabel", 
    anchor="center"
)
lbl_titulo.pack(fill=tk.X, pady=5)

lbl_subtitulo = ttk.Label(
    frame_cabecalho, 
    text="Análise de Desempenho Escolar (5 Alunos - 3 Avaliações por Aluno)", 
    font=("Segoe UI", 10, "italic"),
    anchor="center"
)
lbl_subtitulo.pack(fill=tk.X)

# Separador visual
ttk.Separator(root, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)


# 2. Painel de Entrada de Dados (Alunos e Notas)
frame_entradas_externo = ttk.LabelFrame(root, text=" Cadastro de Alunos e Notas ", padding=10)
frame_entradas_externo.pack(fill=tk.X, padx=15, pady=5)

# Títulos das colunas no grid de cadastro
lbl_col_aluno = ttk.Label(frame_entradas_externo, text="Nº", font=("Segoe UI", 10, "bold"))
lbl_col_aluno.grid(row=0, column=0, padx=5, pady=5, sticky="w")

lbl_col_nome = ttk.Label(frame_entradas_externo, text="Nome Completo do Aluno", font=("Segoe UI", 10, "bold"))
lbl_col_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

lbl_col_n1 = ttk.Label(frame_entradas_externo, text="Nota 1 (0-10)", font=("Segoe UI", 10, "bold"))
lbl_col_n1.grid(row=0, column=2, padx=5, pady=5, sticky="we")

lbl_col_n2 = ttk.Label(frame_entradas_externo, text="Nota 2 (0-10)", font=("Segoe UI", 10, "bold"))
lbl_col_n2.grid(row=0, column=3, padx=5, pady=5, sticky="we")

lbl_col_n3 = ttk.Label(frame_entradas_externo, text="Nota 3 (0-10)", font=("Segoe UI", 10, "bold"))
lbl_col_n3.grid(row=0, column=4, padx=5, pady=5, sticky="we")

# [REPETIÇÃO] Montagem dinâmica das 5 linhas de entrada (uma para cada aluno)
for i in range(5):
    # Número indicador da linha do aluno
    lbl_num = ttk.Label(frame_entradas_externo, text=f"{i+1}º", font=("Segoe UI", 10, "bold"))
    lbl_num.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
    
    # Campo de Entrada para o Nome do Aluno
    ent_nome = ttk.Entry(frame_entradas_externo, width=32, font=("Segoe UI", 10))
    ent_nome.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
    widget_entradas_nomes.append(ent_nome)  # Armazena referência
    
    # Lista auxiliar para armazenar as 3 entradas de notas do aluno atual
    notas_do_aluno_widgets = []
    
    for j in range(3):
        # Campo de Entrada para Nota (Nota 1, Nota 2 e Nota 3)
        ent_nota = ttk.Entry(frame_entradas_externo, width=10, font=("Segoe UI", 10), justify="center")
        ent_nota.grid(row=i+1, column=j+2, padx=8, pady=5)
        notas_do_aluno_widgets.append(ent_nota)  # Armazena referência da nota
        
    widget_entradas_notas.append(notas_do_aluno_widgets)  # Armazena a lista de notas do aluno atual


# 3. Painel de Ações (Botões de Controle)
frame_botoes = ttk.Frame(root, padding=5)
frame_botoes.pack(fill=tk.X, padx=15, pady=5)

# Botão para Executar os Cálculos
btn_calcular = ttk.Button(
    frame_botoes, 
    text="Calcular Resultados", 
    command=calcular_resultados
)
btn_calcular.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

# Botão para Limpar e Resetar a Tela
btn_limpar = ttk.Button(
    frame_botoes, 
    text="Limpar Dados", 
    command=limpar_dados
)
btn_limpar.pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)


# 4. Painel de Resultados Individuais (Tabela Treeview)
frame_resultados = ttk.LabelFrame(root, text=" Resultados Individuais (Médias e Situações) ", padding=10)
frame_resultados.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

# Definição das colunas da tabela
colunas = ("aluno", "n1", "n2", "n3", "media", "situacao")
tree_resultados = ttk.Treeview(frame_resultados, columns=colunas, show="headings")

# Definição dos Cabeçalhos das Colunas
tree_resultados.heading("aluno", text="Aluno")
tree_resultados.heading("n1", text="N1")
tree_resultados.heading("n2", text="N2")
tree_resultados.heading("n3", text="N3")
tree_resultados.heading("media", text="Média Final")
tree_resultados.heading("situacao", text="Situação")

# Ajuste de largura e alinhamento das colunas
tree_resultados.column("aluno", width=220, anchor="w")
tree_resultados.column("n1", width=70, anchor="center")
tree_resultados.column("n2", width=70, anchor="center")
tree_resultados.column("n3", width=70, anchor="center")
tree_resultados.column("media", width=95, anchor="center")
tree_resultados.column("situacao", width=120, anchor="center")

# Barra de rolagem vertical para a tabela
scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=tree_resultados.yview)
tree_resultados.configure(yscrollcommand=scrollbar.set)

tree_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# 5. Painel de Resumo Estatístico da Turma
frame_resumo = ttk.LabelFrame(root, text=" Resumo Estatístico da Turma ", padding=10)
frame_resumo.pack(fill=tk.X, padx=15, pady=10)

# Estruturação em colunas/linhas para visualização limpa
# Coluna 1: Média Geral da Turma e Quantidade de Aprovados/Reprovados
lbl_media_turma_txt = ttk.Label(frame_resumo, text="Média Geral da Turma: ", font=("Segoe UI", 10, "bold"))
lbl_media_turma_txt.grid(row=0, column=0, padx=5, pady=4, sticky="w")
lbl_media_turma_val = ttk.Label(frame_resumo, text="-", font=("Segoe UI", 10, "bold"), foreground="#1e3d59")
lbl_media_turma_val.grid(row=0, column=1, padx=5, pady=4, sticky="w")

lbl_aprovados_txt = ttk.Label(frame_resumo, text="Total de Aprovados (Nota >= 6.0): ", font=("Segoe UI", 10))
lbl_aprovados_txt.grid(row=1, column=0, padx=5, pady=4, sticky="w")
lbl_aprovados_val = ttk.Label(frame_resumo, text="-", font=("Segoe UI", 10, "bold"), foreground="#1b5e20")
lbl_aprovados_val.grid(row=1, column=1, padx=5, pady=4, sticky="w")

lbl_reprovados_txt = ttk.Label(frame_resumo, text="Total de Reprovados (Nota < 6.0): ", font=("Segoe UI", 10))
lbl_reprovados_txt.grid(row=2, column=0, padx=5, pady=4, sticky="w")
lbl_reprovados_val = ttk.Label(frame_resumo, text="-", font=("Segoe UI", 10, "bold"), foreground="#b71c1c")
lbl_reprovados_val.grid(row=2, column=1, padx=5, pady=4, sticky="w")

# Espaçador vertical invisível entre colunas
frame_resumo.columnconfigure(2, minsize=40)

# Coluna 2: Maiores e Menores Médias alcançadas
lbl_maior_media_txt = ttk.Label(frame_resumo, text="Maior Média Obtida: ", font=("Segoe UI", 10))
lbl_maior_media_txt.grid(row=0, column=3, padx=5, pady=4, sticky="w")
lbl_maior_media_val = ttk.Label(frame_resumo, text="-", font=("Segoe UI", 10, "bold"), foreground="#1e3d59")
lbl_maior_media_val.grid(row=0, column=4, padx=5, pady=4, sticky="w")

lbl_menor_media_txt = ttk.Label(frame_resumo, text="Menor Média Obtida: ", font=("Segoe UI", 10))
lbl_menor_media_txt.grid(row=1, column=3, padx=5, pady=4, sticky="w")
lbl_menor_media_val = ttk.Label(frame_resumo, text="-", font=("Segoe UI", 10, "bold"), foreground="#1e3d59")
lbl_menor_media_val.grid(row=1, column=4, padx=5, pady=4, sticky="w")


# ==============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==============================================================================
# Define o foco do teclado para facilitar o início da digitação no campo do Aluno 1
widget_entradas_nomes[0].focus_set()

# Mantém a janela aberta respondendo a eventos (Loop Principal de Eventos)
# Por debaixo dos panos, o método "mainloop()" é uma estrutura de repetição contínua
# que monitora as ações do usuário (clique, digitação, redimensionamento) e atualiza
# os frames na tela em tempo real até que a janela seja fechada.
root.mainloop()
