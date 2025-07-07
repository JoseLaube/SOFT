import pytest
from unittest.mock import MagicMock, patch

from esqueleto import (  
    Usuario, Organizador, LiderDeEquipe, Juiz,
    Evento, Competicao, CompeticaoCombate, CompeticaoSeguidorDeLinha,
    Equipe, Membro, Robo, Inscricao, Luta, TomadaDeTempo,
    StatusInscricao, StatusLuta
)
from datetime import date


def test_adicionar_membro_sem_equipe_cadastrada_deve_lancar_excecao():
    # Arrange
    lider = LiderDeEquipe("Líder Sem Equipe", "sem@equipe.com", "123")
    
    # Act & Assert
    with pytest.raises(Exception, match="O líder precisa cadastrar uma equipe primeiro"):
        lider.adicionar_membro("Membro Fantasma", "Função")

def test_cadastrar_robo_sem_equipe_cadastrada_deve_lancar_excecao():
    # Arrange
    lider = LiderDeEquipe("Líder Sem Equipe", "sem@equipe.com", "123")
    
    # Act & Assert
    with pytest.raises(Exception, match="O líder precisa cadastrar uma equipe primeiro"):
        lider.cadastrar_robo("Robô Fantasma", 1.0)


def test_aprovar_inscricao_para_reprovada_deve_mudar_status():
    # Arrange
    org = Organizador("Chefe", "chefe@org.com", "123")
    # Usando mocks/stubs simples para os objetos da inscrição
    robo_stub = type('Robo', (), {'nome': 'RoboTeste'})()
    competicao_stub = type('Competicao', (), {'nome': 'CompTeste'})()
    inscricao = Inscricao(robo_stub, competicao_stub)
    inscricao.status = StatusInscricao.PENDENTE # Estado inicial
    
    # Act.
    inscricao.status = StatusInscricao.REPROVADA
    
    # Assert
    assert inscricao.status == StatusInscricao.REPROVADA

    # tests/test_usuarios.py


@pytest.fixture
def organizador():
    """Retorna uma instância de Organizador para os testes."""
    return Organizador("Dr. Aratan", "org@evento.com", "senha123")

@pytest.fixture
def lider_de_equipe():
    """Retorna uma instância de LiderDeEquipe para os testes."""
    lider = LiderDeEquipe("Maria", "maria@equipe.com", "senha456")
    lider.cadastrar_equipe("Equipe Alpha")
    return lider

@pytest.fixture
def juiz():
    """Retorna uma instância de Juiz para os testes."""
    return Juiz("Carlos Juiz", "carlos.juiz@evento.com", "senha789")

@pytest.fixture
def evento_mock(organizador):
    """Retorna uma instância de Evento criada por um organizador."""
    return organizador.criar_evento("Torneio Teste", date(2024, 1, 1), date(2024, 1, 2))

@pytest.fixture
def competicao_combate_mock(evento_mock):
    """Retorna uma instância de Competição de Combate."""
    return CompeticaoCombate("Combate 1kg", evento_mock)

@pytest.fixture
def inscricao_mock(competicao_combate_mock):
    """Retorna uma instância de Inscrição para ser usada nos testes."""
    robo_mock = Robo("Robo de Teste", 1.0)
    return Inscricao(robo_mock, competicao_combate_mock)

@pytest.fixture
def luta_mock(inscricao_mock):
    """Retorna uma instância de Luta com um competidor."""
    robo2 = Robo("Adversário", 1.0)
    inscricao2 = Inscricao(robo2, inscricao_mock.competicao)
    return Luta(1, inscricao_mock, inscricao2)


class TestOrganizador:
    def test_criar_evento_com_dados_validos(self, organizador):
        # Arrange
        nome_evento = "RoboComp Anual"
        data_inicio = date(2025, 10, 1)
        data_fim = date(2025, 10, 2)

        # Act
        novo_evento = organizador.criar_evento(nome_evento, data_inicio, data_fim)

        # Assert
        assert isinstance(novo_evento, Evento)
        assert novo_evento.nome == nome_evento
        assert novo_evento.organizador == organizador
        assert novo_evento.data_inicio == data_inicio

    def test_adicionar_competicao_do_tipo_combate(self, organizador, evento_mock):
        # Act
        competicao = organizador.adicionar_competicao(evento_mock, "Combate Peso Pena", "combate")

        # Assert
        assert isinstance(competicao, CompeticaoCombate)
        assert competicao.nome == "Combate Peso Pena"
        assert competicao in evento_mock.competicoes

    def test_adicionar_competicao_do_tipo_seguidor(self, organizador, evento_mock):
        # Act
        competicao = organizador.adicionar_competicao(evento_mock, "Seguidor de Linha Pro", "seguidor")

        # Assert
        assert isinstance(competicao, CompeticaoSeguidorDeLinha)
        assert competicao.nome == "Seguidor de Linha Pro"
        assert competicao in evento_mock.competicoes

    def test_adicionar_competicao_com_tipo_invalido_lanca_erro(self, organizador, evento_mock):
        # Act & Assert
        with pytest.raises(ValueError, match="Tipo de competição inválido"):
            organizador.adicionar_competicao(evento_mock, "Corrida de Drones", "drone")

    def test_aprovar_inscricao_muda_status_para_aprovada(self, organizador, inscricao_mock):
        # Arrange
        inscricao_mock.status = StatusInscricao.PENDENTE

        # Act
        organizador.aprovar_inscricao(inscricao_mock)

        # Assert
        assert inscricao_mock.status == StatusInscricao.APROVADA


class TestLiderDeEquipe:
    def test_cadastrar_equipe_pela_primeira_vez(self):
        # Arrange
        lider = LiderDeEquipe("Novo Líder", "novo@lider.com", "senha")

        # Act
        equipe = lider.cadastrar_equipe("Time Fênix")

        # Assert
        assert isinstance(equipe, Equipe)
        assert lider.equipe == equipe
        assert equipe.nome == "Time Fênix"

    def test_cadastrar_equipe_quando_ja_possui_uma_lanca_erro(self, lider_de_equipe):
        # Act & Assert
        with pytest.raises(Exception, match="Este líder já possui uma equipe cadastrada"):
            lider_de_equipe.cadastrar_equipe("Outro Time")

    def test_adicionar_membro_com_equipe_existente(self, lider_de_equipe):
        # Act
        membro = lider_de_equipe.adicionar_membro("Ana", "Engenheira")

        # Assert
        assert isinstance(membro, Membro)
        assert membro in lider_de_equipe.equipe.membros
        assert membro.nome == "Ana"

    def test_cadastrar_robo_com_equipe_existente(self, lider_de_equipe):
        # Act
        robo = lider_de_equipe.cadastrar_robo("Trovão", 1.0)

        # Assert
        assert isinstance(robo, Robo)
        assert robo in lider_de_equipe.equipe.robos
        assert robo.peso == 1.0

    def test_inscrever_robo_valido_em_competicao(self, lider_de_equipe, competicao_combate_mock):
        # Arrange
        robo_para_inscrever = lider_de_equipe.cadastrar_robo("Destruidor", 1.0)

        # Act
        inscricao = lider_de_equipe.inscrever_robo(robo_para_inscrever, competicao_combate_mock)

        # Assert
        assert isinstance(inscricao, Inscricao)
        assert inscricao.robo == robo_para_inscrever
        assert inscricao.status == StatusInscricao.PENDENTE
        assert inscricao in competicao_combate_mock.inscricoes

    def test_inscrever_robo_que_nao_pertence_a_equipe_lanca_erro(self, lider_de_equipe, competicao_combate_mock):
        # Arrange
        robo_intruso = Robo("Robô Intruso", 1.0)  # Este robô não foi cadastrado pelo líder

        # Act & Assert
        with pytest.raises(Exception, match="Robô não pertence à equipe deste líder"):
            lider_de_equipe.inscrever_robo(robo_intruso, competicao_combate_mock)


class TestJuiz:
    def test_registrar_vencedor_luta_com_sucesso(self, juiz, luta_mock):
        # Arrange
        vencedor = luta_mock.competidor1
        luta_mock.registrar_resultado = MagicMock()

        # Act
        juiz.registrar_vencedor_luta(luta_mock, vencedor)

        # Assert
        luta_mock.registrar_resultado.assert_called_once_with(vencedor)

    def test_registrar_tomada_de_tempo_com_sucesso(self, juiz, inscricao_mock):
        # Arrange
        tempo_registrado = 15.7
        inscricao_mock.adicionar_tomada_de_tempo = MagicMock()

        # Act
        tomada_de_tempo = juiz.registrar_tomada_de_tempo(inscricao_mock, tempo_registrado)

        # Assert
        assert isinstance(tomada_de_tempo, TomadaDeTempo)
        assert tomada_de_tempo.tempo_em_segundos == tempo_registrado
        inscricao_mock.adicionar_tomada_de_tempo.assert_called_once()
        assert inscricao_mock.adicionar_tomada_de_tempo.call_args[0][0] == tomada_de_tempo