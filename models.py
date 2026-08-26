from datetime import date
from enum import Enum
from typing import List, Optional


class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    URGENTE = "Urgente"


class Status(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluída"


class Tarefa:
    """Representa uma tarefa dentro de um projeto."""

    _contador_id = 1

    def __init__(self, titulo: str, descricao: str, prioridade: Prioridade,
                 data_limite: date, projeto: Optional["Projeto"] = None):
        self.id: int = Tarefa._contador_id
        Tarefa._contador_id += 1
        self.titulo: str = titulo
        self.descricao: str = descricao
        self.prioridade: Prioridade = prioridade
        self.data_limite: date = data_limite
        self.status: Status = Status.PENDENTE
        self.projeto: Optional["Projeto"] = projeto

    def marcar_concluida(self) -> None:
        self.status = Status.CONCLUIDA

    def marcar_em_andamento(self) -> None:
        self.status = Status.EM_ANDAMENTO

    def marcar_pendente(self) -> None:
        self.status = Status.PENDENTE

    def esta_vencida(self) -> bool:
        """Retorna True se a tarefa não está concluída e o prazo já passou."""
        return self.status != Status.CONCLUIDA and date.today() > self.data_limite

    def __str__(self) -> str:
        vencida = " (VENCIDA)" if self.esta_vencida() else ""
        return (f"[{self.id}] {self.titulo} | Prioridade: {self.prioridade.value} | "
                f"Status: {self.status.value} | Prazo: {self.data_limite.strftime('%d/%m/%Y')}{vencida}")


class Projeto:
    """Representa um projeto que agrupa várias tarefas de um usuário."""

    _contador_id = 1

    def __init__(self, nome: str, descricao: str, usuario: "Usuario"):
        self.id: int = Projeto._contador_id
        Projeto._contador_id += 1
        self.nome: str = nome
        self.descricao: str = descricao
        self.data_criacao: date = date.today()
        self.usuario: "Usuario" = usuario
        self.tarefas: List[Tarefa] = []

    def adicionar_tarefa(self, tarefa: Tarefa) -> None:
        tarefa.projeto = self
        self.tarefas.append(tarefa)

    def remover_tarefa(self, tarefa_id: int) -> bool:
        for t in self.tarefas:
            if t.id == tarefa_id:
                self.tarefas.remove(t)
                return True
        return False

    def buscar_tarefa(self, tarefa_id: int) -> Optional[Tarefa]:
        return next((t for t in self.tarefas if t.id == tarefa_id), None)

    def calcular_progresso(self) -> float:
        """Retorna o percentual (0-100) de tarefas concluídas no projeto."""
        if not self.tarefas:
            return 0.0
        concluidas = sum(1 for t in self.tarefas if t.status == Status.CONCLUIDA)
        return (concluidas / len(self.tarefas)) * 100

    def __str__(self) -> str:
        return (f"[{self.id}] {self.nome} - {self.descricao} | "
                f"Criado em: {self.data_criacao.strftime('%d/%m/%Y')} | "
                f"Progresso: {self.calcular_progresso():.1f}% | "
                f"{len(self.tarefas)} tarefa(s)")


class Usuario:
    """Representa um usuário do sistema, dono de vários projetos."""

    _contador_id = 1

    def __init__(self, nome: str, email: str, senha: str):
        self.id: int = Usuario._contador_id
        Usuario._contador_id += 1
        self.nome: str = nome
        self.email: str = email
        self.senha: str = senha
        self.projetos: List[Projeto] = []

    def criar_projeto(self, nome: str, descricao: str) -> Projeto:
        projeto = Projeto(nome, descricao, self)
        self.projetos.append(projeto)
        return projeto

    def listar_projetos(self) -> List[Projeto]:
        return self.projetos

    def remover_projeto(self, projeto_id: int) -> bool:
        for p in self.projetos:
            if p.id == projeto_id:
                self.projetos.remove(p)
                return True
        return False

    def buscar_projeto(self, projeto_id: int) -> Optional[Projeto]:
        return next((p for p in self.projetos if p.id == projeto_id), None)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nome} <{self.email}> - {len(self.projetos)} projeto(s)"
