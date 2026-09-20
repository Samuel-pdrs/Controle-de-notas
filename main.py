# -*- coding: utf-8 -*-
"""
Sistema de Controle de Notas - UEMG Carangola
Paradigma procedural estruturado com Tkinter/ttk.

O sistema permite configurar a turma, cadastrar/editar/remover alunos,
calcular medias, consultar desempenho individual e analisar a turma.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# =====================================================================
# VARIAVEIS GLOBAIS E ESTRUTURAS DE DADOS
# =====================================================================
configuracao_turma = {
    "quantidade_alunos": 5,
    "quantidade_avaliacoes": 3,
    "media_minima": 6.0,
}

# Lista de dicionarios: cada aluno possui nome e lista de notas.
alunos = []
contador_id_aluno = 1
aluno_selecionado_id = None
campos_notas = []

# Referencias globais de interface preenchidas durante a montagem da janela.
root = None
tree_alunos = None
tree_avaliacoes = None
tree_individual = None
frame_campos_notas = None
entry_nome = None
entry_busca = None
label_status = None
labels_dashboard = {}
labels_analise = {}
label_detalhe_nome = None
label_detalhe_media = None
label_detalhe_situacao = None
label_detalhe_alerta = None
label_config_atual = None
notebook = None


# =====================================================================
# FUNCOES AUXILIARES E VALIDACOES
# =====================================================================
def converter_para_float(valor_texto):
    """Converte texto para float aceitando virgula como separador decimal."""
    # strip() remove espacos nas extremidades, substituindo uma verificacao manual caractere a caractere.
    texto_limpo = valor_texto.strip().replace(",", ".")
    return float(texto_limpo)


def formatar_numero(valor):
    """Formata numeros com duas casas decimais."""
    return f"{valor:.2f}"


def calcular_media(notas):
    """Calcula a media aritmetica das notas informadas."""
    if not notas:
        return 0.0
    # sum() totaliza a lista por acumulacao interna, substituindo um loop manual com acumulador.
    # len() retorna a quantidade de itens, substituindo uma contagem manual por repeticao.
    return sum(notas) / len(notas)


def obter_situacao(media):
    """Define a situacao do aluno conforme a media minima configurada."""
    if media >= configuracao_turma["media_minima"]:
        return "APROVADO"
    return "REPROVADO"


def buscar_aluno_por_id(aluno_id):
    """Localiza um aluno pelo identificador interno."""
    for aluno in alunos:
        if aluno["id"] == aluno_id:
            return aluno
    return None


def validar_nota(texto_nota, numero_avaliacao):
    """Valida uma nota individual e retorna o valor numerico."""
    if texto_nota.strip() == "":
        raise ValueError(f"Informe a nota da avaliacao {numero_avaliacao}.)")

    try:
        nota = converter_para_float(texto_nota)
    except ValueError as erro:
        raise ValueError(f"Informe uma nota numerica valida na avaliacao {numero_avaliacao}.") from erro

    if nota < 0.0 or nota > 10.0:
        raise ValueError(f"Informe uma nota entre 0 e 10 na avaliacao {numero_avaliacao}.)")

    return nota


def coletar_dados_formulario():
    """Coleta e valida nome e notas do formulario de cadastro/edicao."""
    nome = entry_nome.get().strip()
    if nome == "":
        raise ValueError("Informe o nome do aluno.")

    notas = []
    for indice in range(configuracao_turma["quantidade_avaliacoes"]):
        nota = validar_nota(campos_notas[indice].get(), indice + 1)
        notas.append(nota)

    return nome, notas


def definir_status(mensagem):
    """Exibe feedback curto ao usuario."""
    label_status.config(text=mensagem)


# =====================================================================
# FUNCOES DE ANALISE E ATUALIZACAO DA INTERFACE
# =====================================================================
def calcular_estatisticas():
    """Calcula indicadores reais da turma a partir dos alunos cadastrados."""
    total_alunos = len(alunos)
    medias = []
    aprovados = 0
    reprovados = 0

    for aluno in alunos:
        media = calcular_media(aluno["notas"])
        medias.append(media)
        if obter_situacao(media) == "APROVADO":
            aprovados += 1
        else:
            reprovados += 1

    if total_alunos == 0:
        return {
            "total_alunos": 0,
            "media_geral": 0.0,
            "maior_media": 0.0,
            "menor_media": 0.0,
            "aprovados": 0,
            "reprovados": 0,
            "percentual_aprovacao": 0.0,
            "percentual_reprovacao": 0.0,
        }

    # sum(), max() e min() substituem loops manuais de acumulacao e comparacao linear.
    media_geral = sum(medias) / len(medias)
    maior_media = max(medias)
    menor_media = min(medias)

    return {
        "total_alunos": total_alunos,
        "media_geral": media_geral,
        "maior_media": maior_media,
        "menor_media": menor_media,
        "aprovados": aprovados,
        "reprovados": reprovados,
        "percentual_aprovacao": (aprovados / total_alunos) * 100,
        "percentual_reprovacao": (reprovados / total_alunos) * 100,
    }


def calcular_medias_por_avaliacao():
    """Calcula a media da turma para cada avaliacao configurada."""
    medias_avaliacoes = []
    for indice_avaliacao in range(configuracao_turma["quantidade_avaliacoes"]):
        soma = 0.0
        quantidade = 0
        for aluno in alunos:
            if indice_avaliacao < len(aluno["notas"]):
                soma += aluno["notas"][indice_avaliacao]
                quantidade += 1
        if quantidade > 0:
            medias_avaliacoes.append(soma / quantidade)
        else:
            medias_avaliacoes.append(0.0)
    return medias_avaliacoes


def atualizar_colunas_tabela():
    """Recria colunas da tabela conforme a quantidade de avaliacoes."""
    colunas = ["nome"]
    for indice in range(configuracao_turma["quantidade_avaliacoes"]):
        colunas.append(f"n{indice + 1}")
    colunas.extend(["media", "situacao"])

    tree_alunos.config(columns=colunas)
    tree_alunos.heading("nome", text="Aluno")
    tree_alunos.column("nome", width=220, minwidth=160, anchor="w", stretch=True)

    for indice in range(configuracao_turma["quantidade_avaliacoes"]):
        coluna = f"n{indice + 1}"
        tree_alunos.heading(coluna, text=f"N{indice + 1}")
        tree_alunos.column(coluna, width=75, minwidth=60, anchor="center", stretch=False)

    tree_alunos.heading("media", text="Media")
    tree_alunos.column("media", width=90, minwidth=80, anchor="center", stretch=False)
    tree_alunos.heading("situacao", text="Situacao")
    tree_alunos.column("situacao", width=120, minwidth=100, anchor="center", stretch=False)


def atualizar_tabela_alunos():
    """Atualiza a tabela com os dados reais e filtro de busca."""
    termo_busca = entry_busca.get().strip().lower()

    for item in tree_alunos.get_children():
        tree_alunos.delete(item)

    for aluno in alunos:
        nome_minusculo = aluno["nome"].lower()
        # in verifica pertencimento fazendo busca sequencial na string.
        if termo_busca != "" and termo_busca not in nome_minusculo:
            continue

        media = calcular_media(aluno["notas"])
        situacao = obter_situacao(media)
        valores = [aluno["nome"]]
        for nota in aluno["notas"]:
            valores.append(formatar_numero(nota))
        valores.append(formatar_numero(media))
        valores.append(situacao)
        tree_alunos.insert("", tk.END, iid=str(aluno["id"]), values=valores, tags=(situacao.lower(),))

    tree_alunos.tag_configure("aprovado", foreground="#0f6b3a")
    tree_alunos.tag_configure("reprovado", foreground="#a12424")


def atualizar_dashboard():
    """Atualiza cards e indicadores principais."""
    estatisticas = calcular_estatisticas()
    labels_dashboard["alunos"].config(text=str(estatisticas["total_alunos"]))
    labels_dashboard["media"].config(text=formatar_numero(estatisticas["media_geral"]))
    labels_dashboard["aprovados"].config(text=str(estatisticas["aprovados"]))
    labels_dashboard["reprovados"].config(text=str(estatisticas["reprovados"]))

    labels_analise["media_geral"].config(text=formatar_numero(estatisticas["media_geral"]))
    labels_analise["maior_media"].config(text=formatar_numero(estatisticas["maior_media"]))
    labels_analise["menor_media"].config(text=formatar_numero(estatisticas["menor_media"]))
    labels_analise["aprovados"].config(text=f"{estatisticas['aprovados']} ({estatisticas['percentual_aprovacao']:.1f}%)")
    labels_analise["reprovados"].config(text=f"{estatisticas['reprovados']} ({estatisticas['percentual_reprovacao']:.1f}%)")
    labels_analise["avaliacoes"].config(text=str(configuracao_turma["quantidade_avaliacoes"]))
    labels_analise["capacidade"].config(text=str(configuracao_turma["quantidade_alunos"]))
    labels_analise["media_minima"].config(text=formatar_numero(configuracao_turma["media_minima"]))

    ocupacao = f"{estatisticas['total_alunos']} de {configuracao_turma['quantidade_alunos']} alunos cadastrados"
    labels_dashboard["ocupacao"].config(text=ocupacao)
    label_config_atual.config(
        text=(
            f"Turma: ate {configuracao_turma['quantidade_alunos']} alunos | "
            f"{configuracao_turma['quantidade_avaliacoes']} avaliacoes | "
            f"media minima {formatar_numero(configuracao_turma['media_minima'])}"
        )
    )


def atualizar_analise_avaliacoes():
    """Atualiza tabela de medias por avaliacao."""
    for item in tree_avaliacoes.get_children():
        tree_avaliacoes.delete(item)

    medias = calcular_medias_por_avaliacao()
    for indice, media in enumerate(medias):
        tree_avaliacoes.insert("", tk.END, values=(f"Avaliacao {indice + 1}", formatar_numero(media)))


def atualizar_detalhe_individual(aluno):
    """Mostra detalhes do aluno selecionado."""
    for item in tree_individual.get_children():
        tree_individual.delete(item)

    if aluno is None:
        label_detalhe_nome.config(text="Nenhum aluno selecionado")
        label_detalhe_media.config(text="Media: -")
        label_detalhe_situacao.config(text="Situacao: -")
        label_detalhe_alerta.config(text="Selecione um aluno na tabela para consultar o desempenho individual.")
        return

    media = calcular_media(aluno["notas"])
    situacao = obter_situacao(media)
    label_detalhe_nome.config(text=aluno["nome"])
    label_detalhe_media.config(text=f"Media: {formatar_numero(media)}")
    label_detalhe_situacao.config(text=f"Situacao: {situacao}")

    if situacao == "APROVADO":
        label_detalhe_alerta.config(text="Desempenho dentro do criterio configurado.")
    else:
        label_detalhe_alerta.config(text="Aluno precisa de atencao: media abaixo do criterio configurado.")

    for indice, nota in enumerate(aluno["notas"]):
        tree_individual.insert("", tk.END, values=(f"Avaliacao {indice + 1}", formatar_numero(nota)))


def atualizar_interface_completa():
    """Mantem todas as areas consistentes apos qualquer alteracao."""
    atualizar_colunas_tabela()
    atualizar_tabela_alunos()
    atualizar_dashboard()
    atualizar_analise_avaliacoes()
    atualizar_detalhe_individual(buscar_aluno_por_id(aluno_selecionado_id))


# =====================================================================
# FUNCOES DE CADASTRO, EDICAO, REMOCAO E CONSULTA
# =====================================================================
def limpar_formulario():
    """Limpa campos de entrada e remove selecao atual."""
    global aluno_selecionado_id
    aluno_selecionado_id = None
    entry_nome.delete(0, tk.END)
    for campo in campos_notas:
        campo.delete(0, tk.END)
    tree_alunos.selection_remove(tree_alunos.selection())
    atualizar_detalhe_individual(None)
    definir_status("Formulario pronto para novo cadastro.")


def adicionar_aluno():
    """Adiciona aluno se houver capacidade disponivel na turma."""
    global contador_id_aluno
    if len(alunos) >= configuracao_turma["quantidade_alunos"]:
        messagebox.showwarning("Limite da turma", "A quantidade maxima de alunos configurada ja foi atingida.")
        return

    try:
        nome, notas = coletar_dados_formulario()
    except ValueError as erro:
        messagebox.showerror("Dados invalidos", str(erro))
        return

    alunos.append({"id": contador_id_aluno, "nome": nome, "notas": notas})
    contador_id_aluno += 1
    limpar_formulario()
    atualizar_interface_completa()
    definir_status("Aluno cadastrado com sucesso.")


def editar_aluno():
    """Atualiza nome e notas do aluno selecionado."""
    aluno = buscar_aluno_por_id(aluno_selecionado_id)
    if aluno is None:
        messagebox.showwarning("Selecao necessaria", "Selecione um aluno para editar.")
        return

    try:
        nome, notas = coletar_dados_formulario()
    except ValueError as erro:
        messagebox.showerror("Dados invalidos", str(erro))
        return

    aluno["nome"] = nome
    aluno["notas"] = notas
    atualizar_interface_completa()
    definir_status("Notas atualizadas com sucesso.")


def remover_aluno():
    """Remove aluno selecionado apos confirmacao."""
    global aluno_selecionado_id
    aluno = buscar_aluno_por_id(aluno_selecionado_id)
    if aluno is None:
        messagebox.showwarning("Selecao necessaria", "Selecione um aluno para remover.")
        return

    confirmar = messagebox.askyesno("Confirmar exclusao", f"Deseja realmente excluir o aluno '{aluno['nome']}'?")
    if not confirmar:
        return

    alunos.remove(aluno)
    aluno_selecionado_id = None
    limpar_formulario()
    atualizar_interface_completa()
    definir_status("Aluno removido com sucesso.")


def ao_selecionar_aluno(event=None):
    """Carrega dados do aluno selecionado para consulta e edicao."""
    global aluno_selecionado_id
    selecao = tree_alunos.selection()
    if not selecao:
        return

    aluno_selecionado_id = int(selecao[0])
    aluno = buscar_aluno_por_id(aluno_selecionado_id)
    if aluno is None:
        return

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, aluno["nome"])

    for indice, campo in enumerate(campos_notas):
        campo.delete(0, tk.END)
        if indice < len(aluno["notas"]):
            campo.insert(0, formatar_numero(aluno["notas"][indice]))

    atualizar_detalhe_individual(aluno)
    definir_status("Aluno selecionado para consulta ou edicao.")


def filtrar_alunos(event=None):
    """Aplica pesquisa na tabela de alunos."""
    atualizar_tabela_alunos()


def limpar_todos_os_dados():
    """Remove todos os alunos apos confirmacao."""
    global aluno_selecionado_id
    if not alunos:
        messagebox.showinfo("Sem dados", "Nao existem alunos cadastrados para limpar.")
        return

    confirmar = messagebox.askyesno("Limpar dados", "Deseja realmente remover todos os alunos cadastrados?")
    if not confirmar:
        return

    alunos.clear()
    aluno_selecionado_id = None
    limpar_formulario()
    atualizar_interface_completa()
    definir_status("Todos os dados foram removidos.")


# =====================================================================
# CONFIGURACAO DINAMICA DA TURMA
# =====================================================================
def ajustar_notas_apos_configuracao(nova_quantidade_avaliacoes):
    """Adapta as notas existentes quando a quantidade de avaliacoes muda."""
    for aluno in alunos:
        quantidade_atual = len(aluno["notas"])
        if quantidade_atual < nova_quantidade_avaliacoes:
            for _ in range(nova_quantidade_avaliacoes - quantidade_atual):
                aluno["notas"].append(0.0)
        elif quantidade_atual > nova_quantidade_avaliacoes:
            aluno["notas"] = aluno["notas"][:nova_quantidade_avaliacoes]


def reconstruir_campos_notas():
    """Recria campos de notas no formulario conforme a configuracao."""
    campos_notas.clear()
    for widget in frame_campos_notas.winfo_children():
        widget.destroy()

    for indice in range(configuracao_turma["quantidade_avaliacoes"]):
        linha = indice // 4
        coluna = indice % 4
        frame_campo = ttk.Frame(frame_campos_notas)
        frame_campo.grid(row=linha, column=coluna, sticky="ew", padx=6, pady=5)
        ttk.Label(frame_campo, text=f"Nota {indice + 1}").pack(anchor="w")
        campo = ttk.Entry(frame_campo, width=12, justify="center")
        campo.pack(fill=tk.X)
        campos_notas.append(campo)


def abrir_configuracao_turma():
    """Abre janela para configurar alunos, avaliacoes e media minima."""
    janela = tk.Toplevel(root)
    janela.title("Configurar Turma")
    janela.transient(root)
    janela.grab_set()
    janela.resizable(False, False)

    frame = ttk.Frame(janela, padding=18)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Configuracao da Turma", style="Subtitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    ttk.Label(frame, text="Quantidade de alunos:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
    entrada_alunos = ttk.Entry(frame, width=12)
    entrada_alunos.grid(row=1, column=1, sticky="w", pady=6)
    entrada_alunos.insert(0, str(configuracao_turma["quantidade_alunos"]))

    ttk.Label(frame, text="Quantidade de avaliacoes:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)
    entrada_avaliacoes = ttk.Entry(frame, width=12)
    entrada_avaliacoes.grid(row=2, column=1, sticky="w", pady=6)
    entrada_avaliacoes.insert(0, str(configuracao_turma["quantidade_avaliacoes"]))

    ttk.Label(frame, text="Media minima:").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)
    entrada_media = ttk.Entry(frame, width=12)
    entrada_media.grid(row=3, column=1, sticky="w", pady=6)
    entrada_media.insert(0, formatar_numero(configuracao_turma["media_minima"]))

    def salvar_configuracao():
        try:
            qtd_alunos = int(entrada_alunos.get().strip())
            qtd_avaliacoes = int(entrada_avaliacoes.get().strip())
            media_minima = converter_para_float(entrada_media.get())
        except ValueError:
            messagebox.showerror("Configuracao invalida", "Informe valores numericos validos.")
            return

        if qtd_alunos < 1 or qtd_alunos > 200:
            messagebox.showerror("Configuracao invalida", "A quantidade de alunos deve estar entre 1 e 200.")
            return
        if qtd_avaliacoes < 1 or qtd_avaliacoes > 12:
            messagebox.showerror("Configuracao invalida", "A quantidade de avaliacoes deve estar entre 1 e 12.")
            return
        if media_minima < 0.0 or media_minima > 10.0:
            messagebox.showerror("Configuracao invalida", "A media minima deve estar entre 0 e 10.")
            return
        if len(alunos) > qtd_alunos:
            messagebox.showerror(
                "Configuracao invalida",
                "A nova quantidade de alunos nao pode ser menor que o total ja cadastrado.",
            )
            return

        if qtd_avaliacoes != configuracao_turma["quantidade_avaliacoes"] and alunos:
            confirmar = messagebox.askyesno(
                "Alterar avaliacoes",
                "Alterar a quantidade de avaliacoes adaptara as notas existentes. Deseja continuar?",
            )
            if not confirmar:
                return

        configuracao_turma["quantidade_alunos"] = qtd_alunos
        configuracao_turma["quantidade_avaliacoes"] = qtd_avaliacoes
        configuracao_turma["media_minima"] = media_minima
        ajustar_notas_apos_configuracao(qtd_avaliacoes)
        reconstruir_campos_notas()
        limpar_formulario()
        atualizar_interface_completa()
        definir_status("Configuracao da turma atualizada.")
        janela.destroy()

    botoes = ttk.Frame(frame)
    botoes.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(14, 0))
    ttk.Button(botoes, text="Cancelar", command=janela.destroy).pack(side=tk.RIGHT, padx=4)
    ttk.Button(botoes, text="Salvar configuracao", command=salvar_configuracao, style="Accent.TButton").pack(side=tk.RIGHT, padx=4)


# =====================================================================
# MONTAGEM DA INTERFACE GRAFICA
# =====================================================================
def criar_card(pai, titulo, chave, coluna):
    """Cria card do dashboard."""
    card = ttk.Frame(pai, style="Card.TFrame", padding=16)
    card.grid(row=0, column=coluna, sticky="nsew", padx=6, pady=6)
    pai.columnconfigure(coluna, weight=1)
    ttk.Label(card, text=titulo, style="CardTitle.TLabel").pack(anchor="w")
    valor = ttk.Label(card, text="0", style="CardValue.TLabel")
    valor.pack(anchor="w", pady=(8, 0))
    labels_dashboard[chave] = valor


def criar_linha_analise(pai, texto, chave, linha):
    """Cria uma linha de indicador analitico."""
    ttk.Label(pai, text=texto).grid(row=linha, column=0, sticky="w", padx=8, pady=5)
    valor = ttk.Label(pai, text="-", style="Value.TLabel")
    valor.grid(row=linha, column=1, sticky="w", padx=8, pady=5)
    labels_analise[chave] = valor


def construir_interface():
    """Monta a janela principal e todos os paineis."""
    global root, tree_alunos, tree_avaliacoes, tree_individual, frame_campos_notas
    global entry_nome, entry_busca, label_status, label_detalhe_nome
    global label_detalhe_media, label_detalhe_situacao, label_detalhe_alerta
    global label_config_atual, notebook

    root = tk.Tk()
    root.title("Controle Academico de Notas")
    root.geometry("1120x760")
    root.minsize(940, 640)

    style = ttk.Style()
    style.theme_use("vista" if "vista" in style.theme_names() else "clam")
    style.configure("TFrame", background="#eef3f8")
    style.configure("Card.TFrame", background="#ffffff", relief="flat")
    style.configure("TLabel", background="#eef3f8", font=("Segoe UI", 10))
    style.configure("CardTitle.TLabel", background="#ffffff", foreground="#596579", font=("Segoe UI", 10, "bold"))
    style.configure("CardValue.TLabel", background="#ffffff", foreground="#19324d", font=("Segoe UI", 22, "bold"))
    style.configure("Title.TLabel", background="#eef3f8", foreground="#17324d", font=("Segoe UI", 20, "bold"))
    style.configure("Subtitle.TLabel", background="#eef3f8", foreground="#34495e", font=("Segoe UI", 12, "bold"))
    style.configure("Value.TLabel", background="#eef3f8", foreground="#17324d", font=("Segoe UI", 10, "bold"))
    style.configure("TButton", font=("Segoe UI", 10), padding=7)
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=7)
    style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    cabecalho = ttk.Frame(root, padding=(18, 14, 18, 8))
    cabecalho.grid(row=0, column=0, sticky="ew")
    cabecalho.columnconfigure(0, weight=1)
    ttk.Label(cabecalho, text="Controle Academico de Notas", style="Title.TLabel").grid(row=0, column=0, sticky="w")
    label_config_atual = ttk.Label(cabecalho, text="", foreground="#596579")
    label_config_atual.grid(row=1, column=0, sticky="w", pady=(4, 0))
    ttk.Button(cabecalho, text="Configurar Turma", command=abrir_configuracao_turma, style="Accent.TButton").grid(row=0, column=1, rowspan=2, sticky="e")

    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew", padx=14, pady=8)

    aba_principal = ttk.Frame(notebook, padding=12)
    aba_analises = ttk.Frame(notebook, padding=12)
    aba_individual = ttk.Frame(notebook, padding=12)
    notebook.add(aba_principal, text="Dashboard e Alunos")
    notebook.add(aba_analises, text="Analises da Turma")
    notebook.add(aba_individual, text="Aluno Individual")

    aba_principal.columnconfigure(0, weight=1)
    aba_principal.rowconfigure(2, weight=1)

    dashboard = ttk.Frame(aba_principal)
    dashboard.grid(row=0, column=0, sticky="ew")
    criar_card(dashboard, "Alunos", "alunos", 0)
    criar_card(dashboard, "Media da turma", "media", 1)
    criar_card(dashboard, "Aprovados", "aprovados", 2)
    criar_card(dashboard, "Reprovados", "reprovados", 3)

    labels_dashboard["ocupacao"] = ttk.Label(aba_principal, text="", foreground="#596579")
    labels_dashboard["ocupacao"].grid(row=1, column=0, sticky="w", padx=6, pady=(0, 8))

    corpo = ttk.PanedWindow(aba_principal, orient=tk.HORIZONTAL)
    corpo.grid(row=2, column=0, sticky="nsew")

    painel_form = ttk.LabelFrame(corpo, text="Cadastro e Edicao", padding=12)
    painel_tabela = ttk.LabelFrame(corpo, text="Tabela de Alunos", padding=12)
    corpo.add(painel_form, weight=1)
    corpo.add(painel_tabela, weight=3)

    painel_form.columnconfigure(0, weight=1)
    ttk.Label(painel_form, text="Nome do aluno").grid(row=0, column=0, sticky="w")
    entry_nome = ttk.Entry(painel_form)
    entry_nome.grid(row=1, column=0, sticky="ew", pady=(2, 10))

    frame_campos_notas = ttk.Frame(painel_form)
    frame_campos_notas.grid(row=2, column=0, sticky="ew")

    botoes_form = ttk.Frame(painel_form)
    botoes_form.grid(row=3, column=0, sticky="ew", pady=(14, 0))
    for coluna in range(2):
        botoes_form.columnconfigure(coluna, weight=1)
    ttk.Button(botoes_form, text="Adicionar", command=adicionar_aluno, style="Accent.TButton").grid(row=0, column=0, sticky="ew", padx=3, pady=3)
    ttk.Button(botoes_form, text="Salvar Edicao", command=editar_aluno).grid(row=0, column=1, sticky="ew", padx=3, pady=3)
    ttk.Button(botoes_form, text="Remover", command=remover_aluno).grid(row=1, column=0, sticky="ew", padx=3, pady=3)
    ttk.Button(botoes_form, text="Novo/Limpar", command=limpar_formulario).grid(row=1, column=1, sticky="ew", padx=3, pady=3)
    ttk.Button(painel_form, text="Limpar todos os dados", command=limpar_todos_os_dados).grid(row=4, column=0, sticky="ew", pady=(10, 0))

    painel_tabela.columnconfigure(0, weight=1)
    painel_tabela.rowconfigure(2, weight=1)
    ttk.Label(painel_tabela, text="Pesquisar aluno").grid(row=0, column=0, sticky="w")
    entry_busca = ttk.Entry(painel_tabela)
    entry_busca.grid(row=1, column=0, sticky="ew", pady=(2, 8))
    entry_busca.bind("<KeyRelease>", filtrar_alunos)

    frame_tree = ttk.Frame(painel_tabela)
    frame_tree.grid(row=2, column=0, sticky="nsew")
    frame_tree.columnconfigure(0, weight=1)
    frame_tree.rowconfigure(0, weight=1)
    tree_alunos = ttk.Treeview(frame_tree, show="headings", selectmode="browse")
    scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree_alunos.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree_alunos.xview)
    tree_alunos.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tree_alunos.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tree_alunos.bind("<<TreeviewSelect>>", ao_selecionar_aluno)

    aba_analises.columnconfigure(0, weight=1)
    aba_analises.columnconfigure(1, weight=1)
    aba_analises.rowconfigure(1, weight=1)
    painel_indicadores = ttk.LabelFrame(aba_analises, text="Indicadores gerais", padding=12)
    painel_indicadores.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
    criar_linha_analise(painel_indicadores, "Media geral:", "media_geral", 0)
    criar_linha_analise(painel_indicadores, "Maior media:", "maior_media", 1)
    criar_linha_analise(painel_indicadores, "Menor media:", "menor_media", 2)
    criar_linha_analise(painel_indicadores, "Aprovados:", "aprovados", 3)
    criar_linha_analise(painel_indicadores, "Reprovados:", "reprovados", 4)
    criar_linha_analise(painel_indicadores, "Avaliacoes:", "avaliacoes", 5)
    criar_linha_analise(painel_indicadores, "Capacidade da turma:", "capacidade", 6)
    criar_linha_analise(painel_indicadores, "Media minima:", "media_minima", 7)

    painel_avaliacoes = ttk.LabelFrame(aba_analises, text="Analise por avaliacao", padding=12)
    painel_avaliacoes.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=(0, 8))
    painel_avaliacoes.columnconfigure(0, weight=1)
    painel_avaliacoes.rowconfigure(0, weight=1)
    tree_avaliacoes = ttk.Treeview(painel_avaliacoes, columns=("avaliacao", "media"), show="headings")
    tree_avaliacoes.heading("avaliacao", text="Avaliacao")
    tree_avaliacoes.heading("media", text="Media")
    tree_avaliacoes.column("avaliacao", width=180, anchor="w")
    tree_avaliacoes.column("media", width=100, anchor="center")
    tree_avaliacoes.grid(row=0, column=0, sticky="nsew")

    painel_orientacao = ttk.LabelFrame(aba_analises, text="Leitura dos dados", padding=12)
    painel_orientacao.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
    ttk.Label(
        painel_orientacao,
        text="As analises sao recalculadas automaticamente sempre que aluno, notas ou criterios mudam.",
        wraplength=420,
    ).pack(anchor="w")

    aba_individual.columnconfigure(0, weight=1)
    aba_individual.rowconfigure(1, weight=1)
    painel_detalhe = ttk.LabelFrame(aba_individual, text="Consulta individual", padding=14)
    painel_detalhe.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    label_detalhe_nome = ttk.Label(painel_detalhe, text="Nenhum aluno selecionado", style="Subtitle.TLabel")
    label_detalhe_nome.pack(anchor="w")
    label_detalhe_media = ttk.Label(painel_detalhe, text="Media: -")
    label_detalhe_media.pack(anchor="w", pady=(8, 0))
    label_detalhe_situacao = ttk.Label(painel_detalhe, text="Situacao: -")
    label_detalhe_situacao.pack(anchor="w")
    label_detalhe_alerta = ttk.Label(painel_detalhe, text="Selecione um aluno na tabela para consultar o desempenho individual.", wraplength=700)
    label_detalhe_alerta.pack(anchor="w", pady=(8, 0))

    frame_individual = ttk.LabelFrame(aba_individual, text="Notas do aluno", padding=12)
    frame_individual.grid(row=1, column=0, sticky="nsew")
    frame_individual.columnconfigure(0, weight=1)
    frame_individual.rowconfigure(0, weight=1)
    tree_individual = ttk.Treeview(frame_individual, columns=("avaliacao", "nota"), show="headings")
    tree_individual.heading("avaliacao", text="Avaliacao")
    tree_individual.heading("nota", text="Nota")
    tree_individual.column("avaliacao", width=220, anchor="w")
    tree_individual.column("nota", width=120, anchor="center")
    tree_individual.grid(row=0, column=0, sticky="nsew")

    label_status = ttk.Label(root, text="Sistema pronto.", padding=(18, 8), foreground="#34495e")
    label_status.grid(row=2, column=0, sticky="ew")

    reconstruir_campos_notas()
    atualizar_interface_completa()


# =====================================================================
# INICIALIZACAO
# =====================================================================
construir_interface()
root.mainloop()
