
from __future__ import annotations
from enum import Enum
from datetime import date, datetime
from abc import ABC, abstractmethod
from typing import List, Optional


class TipoPerfil(Enum):
    ORGANIZADOR = "Organizador"
    LIDER_EQUIPE = "Líder de Equipe"
    JUIZ = "Juiz"

class StatusEvento(Enum):
    PLANEJADO = "Planejado"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"

class StatusCompeticao(Enum):
    INSCRICOES_ABERTAS = "Inscrições Abertas"
    EM_ANDAMENTO = "Em Andamento"
    FINALIZADA = "Finalizada"

class StatusInscricao(Enum):
    PENDENTE = "Pendente"
    APROVADA = "Aprovada"
    REPROVADA = "Reprovada"

class StatusLuta(Enum):
    AGENDADA = "Agendada"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"



class Usuario(ABC):
    """Classe base abstrata para todos os usuários do sistema."""
    def __init__(self, nome: str, email: str, senha: str):
        self.id: int = id(self)  # Simulação de um ID único
        self.nome: str = nome
        self.email: str = email
        self.senha: str = senha  # Em um sistema real, isso seria um hash
        self.data_cadastro: date = date.today()

    def login(self):
        print(f"Usuário {self.nome} logado.")
        pass

    def logout(self):
        print(f"Usuário {self.nome} deslogado.")
        pass

class Organizador(Usuario):
    """Representa um usuário com permissões para gerenciar eventos."""
    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha)
        self.perfil = TipoPerfil.ORGANIZADOR

    def criar_evento(self, nome: str, data_inicio: date, data_fim: date) -> Evento:
        print(f"Organizador {self.nome} criou o evento '{nome}'.")
        novo_evento = Evento(nome, data_inicio, data_fim, self)
        return novo_evento

    def adicionar_competicao(self, evento: Evento, nome: str, tipo: str) -> Competicao:
        print(f"Adicionando competição '{nome}' do tipo '{tipo}' ao evento '{evento.nome}'.")
        if tipo.lower() == 'combate':
            competicao = CompeticaoCombate(nome, evento)
        elif tipo.lower() == 'seguidor':
            competicao = CompeticaoSeguidorDeLinha(nome, evento)
        else:
            raise ValueError("Tipo de competição inválido.")
        
        evento.adicionar_competicao(competicao)
        return competicao

    def aprovar_inscricao(self, inscricao: Inscricao):
        print(f"Avaliando inscrição ID {inscricao.id}.")
        # Lógica para aprovar/reprovar
        inscricao.status = StatusInscricao.APROVADA
        pass

class LiderDeEquipe(Usuario):
    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha)
        self.perfil = TipoPerfil.LIDER_EQUIPE
        self.equipe: Optional[Equipe] = None

    def cadastrar_equipe(self, nome_equipe: str) -> Equipe:
        if not self.equipe:
            print(f"Líder {self.nome} cadastrou a equipe '{nome_equipe}'.")
            self.equipe = Equipe(nome_equipe, self)
            return self.equipe
        else:
            raise Exception("Este líder já possui uma equipe cadastrada.")

    def adicionar_membro(self, nome_membro: str, funcao: str) -> Membro:
        if self.equipe:
            print(f"Adicionando membro {nome_membro} à equipe {self.equipe.nome}.")
            membro = Membro(nome_membro, funcao)
            self.equipe.adicionar_membro(membro)
            return membro
        else:
            raise Exception("O líder precisa cadastrar uma equipe primeiro.")
    
    def cadastrar_robo(self, nome_robo: str, peso: float) -> Robo:
        if self.equipe:
            print(f"Cadastrando robô {nome_robo} para a equipe {self.equipe.nome}.")
            robo = Robo(nome_robo, peso)
            self.equipe.adicionar_robo(robo)
            return robo
        else:
            raise Exception("O líder precisa cadastrar uma equipe primeiro.")

    def inscrever_robo(self, robo: Robo, competicao: Competicao) -> Inscricao:
        if self.equipe and robo in self.equipe.robos:
            print(f"Inscrevendo robô {robo.nome} na competição {competicao.nome}.")
            inscricao = Inscricao(robo, competicao)
            competicao.receber_inscricao(inscricao)
            return inscricao
        else:
            raise Exception("Robô não pertence à equipe deste líder.")


class Juiz(Usuario):
    """Representa um usuário com permissões para registrar resultados."""
    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha)
        self.perfil = TipoPerfil.JUIZ

    def registrar_vencedor_luta(self, luta: Luta, vencedor: Inscricao):
        print(f"Juiz {self.nome} registrou {vencedor.robo.nome} como vencedor da luta ID {luta.id}.")
        luta.registrar_resultado(vencedor)
        # Lógica para avançar na chave de batalha
        pass

    def registrar_tomada_de_tempo(self, inscricao: Inscricao, tempo: float) -> TomadaDeTempo:
        print(f"Juiz {self.nome} registrou o tempo {tempo}s para o robô {inscricao.robo.nome}.")
        tomada = TomadaDeTempo(tempo)
        inscricao.adicionar_tomada_de_tempo(tomada)
        return tomada


class Equipe:
    def __init__(self, nome: str, lider: LiderDeEquipe):
        self.id: int = id(self)
        self.nome: str = nome
        self.data_criacao: date = date.today()
        self.lider: LiderDeEquipe = lider
        self.membros: List[Membro] = []
        self.robos: List[Robo] = []

    def adicionar_membro(self, membro: Membro):
        self.membros.append(membro)

    def adicionar_robo(self, robo: Robo):
        self.robos.append(robo)

class Membro:
    def __init__(self, nome: str, funcao: str):
        self.id: int = id(self)
        self.nome: str = nome
        self.funcao: str = funcao
        self.data_ingresso: date = date.today()

class Robo:
    def __init__(self, nome: str, peso: float):
        self.id: int = id(self)
        self.nome: str = nome
        self.peso: float = peso
        self.disponivel: bool = True
        
class Evento:
    def __init__(self, nome: str, data_inicio: date, data_fim: date, organizador: Organizador):
        self.id: int = id(self)
        self.nome: str = nome
        self.data_inicio: date = data_inicio
        self.data_fim: date = data_fim
        self.status: StatusEvento = StatusEvento.PLANEJADO
        self.organizador: Organizador = organizador
        self.competicoes: List[Competicao] = []

    def adicionar_competicao(self, competicao: Competicao):
        self.competicoes.append(competicao)


class Competicao(ABC):
    """Classe base abstrata para os diferentes tipos de competição."""
    def __init__(self, nome: str, evento: Evento):
        self.id: int = id(self)
        self.nome: str = nome
        self.evento: Evento = evento
        self.status: StatusCompeticao = StatusCompeticao.INSCRICOES_ABERTAS
        self.inscricoes: List[Inscricao] = []
        
    def receber_inscricao(self, inscricao: Inscricao):
        self.inscricoes.append(inscricao)
    
    @abstractmethod
    def gerar_estrutura(self):
        pass

class CompeticaoCombate(Competicao):
    """Representa a categoria de combate."""
    def __init__(self, nome: str, evento: Evento):
        super().__init__(nome, evento)
        self.chave_batalha: Optional[ChaveDeBatalha] = None
    
    def gerar_estrutura(self):
        print(f"Gerando chave de batalha para a competição '{self.nome}'.")
        robos_aprovados = [insc.robo for insc in self.inscricoes if insc.status == StatusInscricao.APROVADA]
        self.chave_batalha = ChaveDeBatalha("Eliminatória Simples", robos_aprovados)
        # Lógica para criar as Lutas
        pass

class CompeticaoSeguidorDeLinha(Competicao):
    def gerar_estrutura(self):
        print(f"Estrutura para '{self.nome}' definida. Competidores prontos para as tomadas de tempo.")
        pass

    def gerar_classificacao(self) -> List[Resultado]:
        """Calcula e gera a tabela de classificação baseada nos melhores tempos."""
        print(f"Gerando classificação para '{self.nome}'.")
        resultados: List[Resultado] = []
        # Lógica para calcular melhor tempo de cada inscrição e ordenar
        return resultados

class Inscricao:
    """Conecta um Robô a uma Competição específica."""
    def __init__(self, robo: Robo, competicao: Competicao):
        self.id: int = id(self)
        self.robo: Robo = robo
        self.competicao: Competicao = competicao
        self.data_inscricao: datetime = datetime.now()
        self.status: StatusInscricao = StatusInscricao.PENDENTE
        self.tomadas_de_tempo: List[TomadaDeTempo] = []
    
    def adicionar_tomada_de_tempo(self, tomada: TomadaDeTempo):
        self.tomadas_de_tempo.append(tomada)
        
    def get_melhor_tempo(self) -> Optional[float]:
        if not self.tomadas_de_tempo:
            return None
        return min(t.tempo_em_segundos for t in self.tomadas_de_tempo)


class ChaveDeBatalha:
    def __init__(self, formato: str, robos_participantes: List[Robo]):
        self.id: int = id(self)
        self.formato: str = formato
        self.lutas: List[Luta] = []
        self.robos_participantes = robos_participantes

    def avancar_vencedor(self, luta: Luta):
        pass

class Luta:
    """Representa uma única batalha entre dois competidores."""
    def __init__(self, rodada: int, competidor1: Inscricao, competidor2: Inscricao):
        self.id: int = id(self)
        self.rodada: int = rodada
        self.status: StatusLuta = StatusLuta.AGENDADA
        self.competidor1: Inscricao = competidor1
        self.competidor2: Inscricao = competidor2
        self.vencedor: Optional[Inscricao] = None

    def registrar_resultado(self, vencedor: Inscricao):
        """Define o vencedor da luta e atualiza o status."""
        if vencedor not in [self.competidor1, self.competidor2]:
            raise ValueError("Vencedor inválido para esta luta.")
        self.vencedor = vencedor
        self.status = StatusLuta.CONCLUIDA

class TomadaDeTempo:
    def __init__(self, tempo_em_segundos: float):
        self.id: int = id(self)
        self.tempo_em_segundos: float = tempo_em_segundos
        self.data_registro: datetime = datetime.now()

class Resultado:
    """Representa uma linha na tabela de classificação final."""
    def __init__(self, posicao: int, inscricao: Inscricao, melhor_tempo: float):
        self.posicao: int = posicao
        self.inscricao: Inscricao = inscricao
        self.melhor_tempo: float = melhor_tempo


class PainelDeVisualizacao:

    def ver_chave_de_batalha(self, competicao: CompeticaoCombate):
        print(f"\n--- PAINEL PÚBLICO: CHAVE DE BATALHA DE '{competicao.nome}' ---")
        if competicao.chave_batalha:
            # Lógica para imprimir a chave de forma visual
            print("Chave de batalha gerada. Lutas a serem exibidas.")
        else:
            print("A chave de batalha ainda não foi gerada.")

    def ver_classificacao_seguidor(self, competicao: CompeticaoSeguidorDeLinha):
        print(f"\n--- PAINEL PÚBLICO: CLASSIFICAÇÃO DE '{competicao.nome}' ---")
        classificacao = competicao.gerar_classificacao()
        if classificacao:
            for res in classificacao:
                print(f"{res.posicao}º: {res.inscricao.robo.nome} ({res.melhor_tempo}s)")
        else:
            print("Classificação ainda não disponível.")
            
    def ver_resultados_evento(self, evento: Evento):
        print(f"\n--- PAINEL PÚBLICO: RESULTADOS DO EVENTO '{evento.nome}' ---")
        for comp in evento.competicoes:
            print(f"Competição: {comp.nome} - Status: {comp.status.value}")
        

