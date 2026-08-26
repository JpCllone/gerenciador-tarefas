from datetime import datetime

from gerenciador import SistemaGerenciador
from models import Prioridade, Status


def ler_data(mensagem: str):
    while True:
        texto = input(mensagem).strip()
        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa (ex: 30/09/2026).")


def escolher_opcao(mensagem: str, opcoes: list) -> int:
    print(mensagem)
    for i, op in enumerate(opcoes, start=1):
        print(f"  {i}. {op}")
    while True:
        escolha = input("Escolha uma opção: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return int(escolha)
        print("Opção inválida, tente novamente.")


def pausar():
    input("\nPressione ENTER para continuar...")


# ------------------------------------------------------------------
# Usuários
# ------------------------------------------------------------------
def menu_usuarios(sistema: SistemaGerenciador):
    while True:
        print("\n--- CADASTRO DE USUÁRIOS ---")
        opcao = escolher_opcao("", [
            "Criar usuário", "Listar usuários", "Remover usuário",
            "Entrar em um usuário (gerenciar projetos)", "Voltar",
        ])
        if opcao == 1:
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            senha = input("Senha: ").strip()
            usuario = sistema.criar_usuario(nome, email, senha)
            print(f"Usuário criado com sucesso! {usuario}")
        elif opcao == 2:
            listar_usuarios(sistema)
        elif opcao == 3:
            listar_usuarios(sistema)
            uid = input("ID do usuário a remover: ").strip()
            if uid.isdigit() and sistema.remover_usuario(int(uid)):
                print("Usuário removido.")
            else:
                print("Usuário não encontrado.")
        elif opcao == 4:
            usuario = selecionar_usuario(sistema)
            if usuario:
                menu_projetos(usuario)
        elif opcao == 5:
            return
        pausar()


def listar_usuarios(sistema: SistemaGerenciador):
    if not sistema.usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in sistema.usuarios:
        print(f"  {u}")


def selecionar_usuario(sistema: SistemaGerenciador):
    listar_usuarios(sistema)
    if not sistema.usuarios:
        return None
    uid = input("ID do usuário: ").strip()
    usuario = sistema.buscar_usuario(int(uid)) if uid.isdigit() else None
    if not usuario:
        print("Usuário não encontrado.")
    return usuario


# ------------------------------------------------------------------
# Projetos
# ------------------------------------------------------------------
def menu_projetos(usuario):
    while True:
        print(f"\n--- PROJETOS DE {usuario.nome} ---")
        opcao = escolher_opcao("", [
            "Criar projeto", "Listar projetos", "Remover projeto",
            "Entrar em um projeto (gerenciar tarefas)", "Voltar",
        ])
        if opcao == 1:
            nome = input("Nome do projeto: ").strip()
            descricao = input("Descrição: ").strip()
            projeto = usuario.criar_projeto(nome, descricao)
            print(f"Projeto criado! {projeto}")
        elif opcao == 2:
            listar_projetos(usuario)
        elif opcao == 3:
            listar_projetos(usuario)
            pid = input("ID do projeto a remover: ").strip()
            if pid.isdigit() and usuario.remover_projeto(int(pid)):
                print("Projeto removido.")
            else:
                print("Projeto não encontrado.")
        elif opcao == 4:
            projeto = selecionar_projeto(usuario)
            if projeto:
                menu_tarefas(projeto)
        elif opcao == 5:
            return
        pausar()


def listar_projetos(usuario):
    if not usuario.projetos:
        print("Nenhum projeto cadastrado.")
        return
    for p in usuario.projetos:
        print(f"  {p}")


def selecionar_projeto(usuario):
    listar_projetos(usuario)
    if not usuario.projetos:
        return None
    pid = input("ID do projeto: ").strip()
    projeto = usuario.buscar_projeto(int(pid)) if pid.isdigit() else None
    if not projeto:
        print("Projeto não encontrado.")
    return projeto


# ------------------------------------------------------------------
# Tarefas
# ------------------------------------------------------------------
def menu_tarefas(projeto):
    while True:
        print(f"\n--- TAREFAS DO PROJETO '{projeto.nome}' ---")
        opcao = escolher_opcao("", [
            "Adicionar tarefa", "Listar tarefas", "Remover tarefa",
            "Atualizar status de uma tarefa", "Ver progresso do projeto", "Voltar",
        ])
        if opcao == 1:
            titulo = input("Título: ").strip()
            descricao = input("Descrição: ").strip()
            prioridades = list(Prioridade)
            idx = escolher_opcao("Prioridade:", [p.value for p in prioridades])
            prioridade = prioridades[idx - 1]
            data_limite = ler_data("Data limite (dd/mm/aaaa): ")
            from models import Tarefa
            tarefa = Tarefa(titulo, descricao, prioridade, data_limite)
            projeto.adicionar_tarefa(tarefa)
            print(f"Tarefa adicionada! {tarefa}")
        elif opcao == 2:
            listar_tarefas(projeto)
        elif opcao == 3:
            listar_tarefas(projeto)
            tid = input("ID da tarefa a remover: ").strip()
            if tid.isdigit() and projeto.remover_tarefa(int(tid)):
                print("Tarefa removida.")
            else:
                print("Tarefa não encontrada.")
        elif opcao == 4:
            listar_tarefas(projeto)
            tid = input("ID da tarefa: ").strip()
            tarefa = projeto.buscar_tarefa(int(tid)) if tid.isdigit() else None
            if not tarefa:
                print("Tarefa não encontrada.")
            else:
                status_opcoes = list(Status)
                idx = escolher_opcao("Novo status:", [s.value for s in status_opcoes])
                novo_status = status_opcoes[idx - 1]
                if novo_status == Status.CONCLUIDA:
                    tarefa.marcar_concluida()
                elif novo_status == Status.EM_ANDAMENTO:
                    tarefa.marcar_em_andamento()
                else:
                    tarefa.marcar_pendente()
                print(f"Status atualizado! {tarefa}")
        elif opcao == 5:
            print(f"Progresso do projeto: {projeto.calcular_progresso():.1f}%")
        elif opcao == 6:
            return
        pausar()


def listar_tarefas(projeto):
    if not projeto.tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for t in projeto.tarefas:
        print(f"  {t}")


# ------------------------------------------------------------------
# Relatórios
# ------------------------------------------------------------------
def menu_relatorios(sistema: SistemaGerenciador):
    while True:
        print("\n--- RELATÓRIOS ---")
        opcao = escolher_opcao("", [
            "Mostrar relatório completo na tela",
            "Exportar relatório para .txt",
            "Exportar relatório para .csv",
            "Voltar",
        ])
        if opcao == 1:
            print("\n" + sistema.gerar_texto_relatorio())
        elif opcao == 2:
            caminho = sistema.exportar_relatorio_txt()
            print(f"Relatório exportado para: {caminho}")
        elif opcao == 3:
            caminho = sistema.exportar_relatorio_csv()
            print(f"Relatório exportado para: {caminho}")
        elif opcao == 4:
            return
        pausar()


# ------------------------------------------------------------------
# Dados de exemplo
# ------------------------------------------------------------------
def carregar_dados_exemplo(sistema: SistemaGerenciador):
    from datetime import date, timedelta
    from models import Tarefa

    u1 = sistema.criar_usuario("Ana Souza", "ana@email.com", "123456")
    p1 = u1.criar_projeto("Trabalho de POO", "Projeto da disciplina de POO")
    t1 = Tarefa("Modelar classes", "Criar diagrama de classes", Prioridade.ALTA,
                date.today() + timedelta(days=2))
    t2 = Tarefa("Implementar sistema", "Codificar o gerenciador", Prioridade.URGENTE,
                date.today() + timedelta(days=1))
    p1.adicionar_tarefa(t1)
    p1.adicionar_tarefa(t2)
    t2.marcar_concluida()


# ------------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------------
def main():
    sistema = SistemaGerenciador()

    print("=" * 60)
    print("   GERENCIADOR INTELIGENTE DE TAREFAS")
    print("=" * 60)
    if input("Carregar dados de exemplo para teste? (s/n): ").strip().lower() == "s":
        carregar_dados_exemplo(sistema)

    while True:
        opcao = escolher_opcao("\n=== MENU PRINCIPAL ===", [
            "Usuários (criar / listar / remover / gerenciar projetos)",
            "Relatórios",
            "Sair",
        ])
        if opcao == 1:
            menu_usuarios(sistema)
        elif opcao == 2:
            menu_relatorios(sistema)
        elif opcao == 3:
            print("Encerrando o sistema. Até logo!")
            break


if __name__ == "__main__":
    main()
