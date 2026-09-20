# MEMORY.md

## Nome e objetivo do projeto
**Sistema de Controle de Notas - UEMG Carangola**

O objetivo do sistema é facilitar o controle de notas de alunos com configuração flexível de turma, realizando cálculos automáticos de médias, determinando a situação de aprovação/reprovação, além de gerar estatísticas e análises da turma.

## Tecnologias utilizadas
- **Linguagem:** Python 3.x
- **Interface Gráfica:** `tkinter` e `tkinter.ttk` (estilo nativo/temático do Windows)

## Estrutura atual do projeto
```
Controle-de-notas/
├── main.py                # Código principal
├── py.md                  # Documentação extra de referência (não identificado)
├── MEMORY.md              # Este arquivo
├── ROADMAP.md             # Planejamento
├── README.md              # Introdução
└── ia/
    └── Prompt Python.md   # Instruções de desenvolvimento
```

## Funcionamento geral
O sistema utiliza paradigma procedural. O usuário configura a turma (quantidade de alunos, avaliações e média mínima), cadastra/edita/remove alunos, e o sistema calcula médias, situações e estatísticas em tempo real. A interface é organizada em abas: Dashboard/Alunos, Análises da Turma e Aluno Individual.

## Organização do código
- **Estrutura de dados:**
    - `configuracao_turma`: dicionário com `quantidade_alunos`, `quantidade_avaliacoes`, `media_minima`.
    - `alunos`: lista de dicionários, cada um com `id`, `nome`, `notas` (lista de floats).
    - `contador_id_aluno`: inteiro para IDs únicos.
    - `aluno_selecionado_id`: ID do aluno selecionado na tabela.
    - `campos_notas`: lista de referências aos widgets Entry de notas (recriados dinamicamente).
- **Interface:** Organizada com `grid`, `pack`, `PanedWindow`, `Notebook`, `Treeview` com scrollbars.
- **Lógica:** Procedural, funções para validação, cálculo, CRUD, atualização de UI e configuração.

## Regras de negócio
- **Média:** Soma das notas dividida pela quantidade de avaliações configurada.
- **Situação:** Média >= `media_minima` (APROVADO), < `media_minima` (REPROVADO).
- **Entrada:** Notas entre 0.0 e 10.0; nome obrigatório; vírgula ou ponto como separador decimal.
- **Capacidade:** Não permite cadastrar mais alunos que o configurado.
- **Ajuste de notas:** Ao alterar quantidade de avaliações, notas existentes são preservadas/ajustadas (preenchidas com 0.0 ou truncadas).

## Decisões importantes
- Paradigma procedural puro (sem `class`), variáveis globais e funções.
- Comentários explicativos para funções nativas de alto nível (`sum`, `max`, `min`, `len`, `in`, `strip`, `replace`).
- Estruturas de Böhm-Jacopini evidentes: Sequência (montagem da UI), Seleção (validações, situações), Repetição (loops sobre alunos/avaliações).
- Configuração dinâmica: a UI se reconstrói ao mudar parâmetros da turma.
- Consistência: `atualizar_interface_completa()` sincroniza todas as abas após qualquer alteração.

## Limitações conhecidas
- Sem persistência de dados (arquivo/banco) — dados perdidos ao fechar.
- Sem exportação (PDF/Excel).
- Sem pesos por avaliação, recuperação, frequência ou exame final.
- Limite de 200 alunos e 12 avaliações na configuração (validação arbitrária).

## Problemas conhecidos
- Nenhum identificado no código atual.

## Dependências importantes
- Python 3.x com `tkinter` (biblioteca padrão).

## Informações para modificação
- O projeto exige paradigma **procedural puro** (sem `class`).
- Todo uso de atalhos/funções de alto nível deve ter comentário explicativo.
- Deve respeitar as estruturas de Böhm-Jacopini (Sequência, Seleção, Repetição).
- `atualizar_interface_completa()` deve ser chamada após qualquer mudança de dados.
- `reconstruir_campos_notas()` recria os campos de nota do formulário.
- `ajustar_notas_apos_configuracao()` adapta notas existentes ao mudar avaliações.
