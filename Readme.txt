# Gerenciador Inteligente de Tarefas

Trabalho da Aula 03 de POO. A proposta era construir um sistema que aplicasse os
conceitos de Programação Orientada a Objetos vistos em aula (classes, atributos,
métodos, relacionamento entre objetos, enums), então foi isso que guiou as
decisões abaixo.

## O que o sistema faz

É um gerenciador de tarefas: um usuário pode criar vários projetos, e dentro de
cada projeto ele cadastra as tarefas, define prioridade e prazo, e vai
atualizando o status conforme avança. No final dá pra ver relatórios de
produtividade e exportar tudo em .txt ou .csv.

## Como organizei o código

Separei em 3 arquivos pra não deixar tudo misturado num arquivo só:

- **models.py** - só as classes de domínio (Usuario, Projeto, Tarefa) e os enums
  (Prioridade, Status). Esse arquivo não sabe nada sobre menu ou interação com o
  usuário, só define como os dados se comportam.
- **gerenciador.py** - a classe SistemaGerenciador, que é quem guarda a lista de
  usuários e centraliza as operações (criar, buscar, remover, gerar relatório,
  exportar). Fiz isso separado das classes de modelo pra não misturar "o que é
  um usuário" com "como o sistema gerencia os usuários".
- **main.py** - só o menu de terminal, ou seja, a parte de interação. Ele chama
  os métodos das outras duas partes, mas não tem lógica de negócio nele.

## Como apliquei POO

- **Usuario, Projeto e Tarefa** são as 3 classes principais, seguindo o
  diagrama passado em aula. Um Usuario tem uma lista de Projetos, e cada
  Projeto tem uma lista de Tarefas - isso é o relacionamento de composição
  (um projeto sem usuário não existe, uma tarefa sem projeto não existe).
- Cada classe cuida dos próprios dados. Por exemplo, quem calcula o progresso
  de conclusão é o próprio Projeto (`calcular_progresso`), não uma função solta
  em outro lugar - isso é encapsulamento, o projeto sabe como calcular o
  progresso dele mesmo.
- **Prioridade** e **Status** viraram Enum ao invés de string solta, pra evitar
  erro de digitação (tipo escrever "Urgente" errado em algum lugar) e deixar
  mais fácil comparar e ordenar.
- A Tarefa tem os métodos `marcar_concluida()`, `marcar_em_andamento()` etc,
  em vez de deixar qualquer parte do código mudar o status dela diretamente -
  assim toda mudança de status passa por um lugar só.

## Relatórios

O SistemaGerenciador varre todos os usuários/projetos/tarefas pra montar 3
relatórios pedidos no enunciado:

1. Tarefas pendentes ordenadas por prioridade (urgente primeiro)
2. Projetos ordenados por % de conclusão
3. Total de tarefas concluídas por usuário

E dá pra exportar esse relatório pronto em `.txt` (texto corrido) ou `.csv`
(uma linha por tarefa, pra abrir em Excel/planilha).

## Como rodar

Só precisa ter Python instalado, não usei nenhuma biblioteca externa:

```
python main.py
```

Ele pergunta se quer carregar dados de exemplo pra já testar rápido (um
usuário com um projeto e duas tarefas). Se responder não, começa vazio e você
cadastra tudo pelo menu mesmo.
