import csv
from datetime import datetime
from typing import Dict, List, Optional

from models import Usuario, Projeto, Tarefa, Prioridade, Status


class SistemaGerenciador:
    def __init__(self):
        self.usuarios: List[Usuario] = []

    # ---------------- Usuários ----------------
    def criar_usuario(self, nome: str, email: str, senha: str) -> Usuario:
        usuario = Usuario(nome, email, senha)
        self.usuarios.append(usuario)
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuarios

    def remover_usuario(self, usuario_id: int) -> bool:
        usuario = self.buscar_usuario(usuario_id)
        if usuario:
            self.usuarios.remove(usuario)
            return True
        return False

    def buscar_usuario(self, usuario_id: int) -> Optional[Usuario]:
        return next((u for u in self.usuarios if u.id == usuario_id), None)

    # ---------------- Relatórios ----------------
    def tarefas_pendentes_por_prioridade(self) -> List[Tarefa]:
        """Todas as tarefas não concluídas, ordenadas da mais urgente para a menos."""
        pendentes = [
            t for u in self.usuarios for p in u.projetos for t in p.tarefas
            if t.status != Status.CONCLUIDA
        ]
        ordem = {Prioridade.URGENTE: 0, Prioridade.ALTA: 1,
                 Prioridade.MEDIA: 2, Prioridade.BAIXA: 3}
        pendentes.sort(key=lambda t: ordem[t.prioridade])
        return pendentes

    def projetos_por_conclusao(self) -> List[Projeto]:
        """Todos os projetos, ordenados pela maior % de conclusão."""
        todos = [p for u in self.usuarios for p in u.projetos]
        todos.sort(key=lambda p: p.calcular_progresso(), reverse=True)
        return todos

    def total_tarefas_concluidas_por_usuario(self) -> Dict[Usuario, int]:
        return {
            u: sum(1 for p in u.projetos for t in p.tarefas if t.status == Status.CONCLUIDA)
            for u in self.usuarios
        }

    def gerar_texto_relatorio(self) -> str:
        linhas = [
            f"RELATÓRIO GERAL - Gerado em {datetime.now():%d/%m/%Y %H:%M}",
            "=" * 60,
            "",
            "TAREFAS PENDENTES POR PRIORIDADE:",
        ]
        pendentes = self.tarefas_pendentes_por_prioridade()
        linhas += [f"  {t}" for t in pendentes] if pendentes else ["  (nenhuma tarefa pendente)"]

        linhas += ["", "PROJETOS POR % DE CONCLUSÃO:"]
        projetos = self.projetos_por_conclusao()
        linhas += [f"  {p}" for p in projetos] if projetos else ["  (nenhum projeto cadastrado)"]

        linhas += ["", "TOTAL DE TAREFAS CONCLUÍDAS POR USUÁRIO:"]
        totais = self.total_tarefas_concluidas_por_usuario()
        if totais:
            linhas += [f"  {u.nome}: {total} concluída(s)" for u, total in totais.items()]
        else:
            linhas.append("  (nenhum usuário cadastrado)")

        return "\n".join(linhas)

    # ---------------- Exportação ----------------
    def exportar_relatorio_txt(self, caminho: str = "relatorio.txt") -> str:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(self.gerar_texto_relatorio())
        return caminho

    def exportar_relatorio_csv(self, caminho: str = "relatorio.csv") -> str:
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Usuario", "Projeto", "Tarefa", "Prioridade", "Status", "Prazo"])
            for u in self.usuarios:
                for p in u.projetos:
                    for t in p.tarefas:
                        writer.writerow([
                            u.nome, p.nome, t.titulo, t.prioridade.value,
                            t.status.value, t.data_limite.strftime("%d/%m/%Y"),
                        ])
        return caminho
