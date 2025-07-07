import pytest
from esqueleto import Luta, Inscricao, Robo, CompeticaoCombate, StatusLuta, TomadaDeTempo
from datetime import datetime

@pytest.fixture
def inscricao_mock_1():
    robo = Robo("Trovão", 1.0)
    competicao = CompeticaoCombate("Combate 1kg", evento=None) 
    return Inscricao(robo, competicao)

@pytest.fixture
def inscricao_mock_2():
    robo = Robo("Relâmpago", 1.0)
    competicao = CompeticaoCombate("Combate 1kg", evento=None)
    return Inscricao(robo, competicao)

def test_registrar_resultado_comVencedorValido_deveDefinirVencedorEStatusConcluida(inscricao_mock_1, inscricao_mock_2):
    # Arrange
    luta = Luta(rodada=1, competidor1=inscricao_mock_1, competidor2=inscricao_mock_2)
    vencedor_esperado = inscricao_mock_1

    # Act
    luta.registrar_resultado(vencedor_esperado)

    # Assert
    assert luta.vencedor == vencedor_esperado
    assert luta.status == StatusLuta.CONCLUIDA

def test_registrar_resultado_comVencedorNaoParticipante_deveLancarValueError(inscricao_mock_1, inscricao_mock_2):
    # Arrange
    luta = Luta(rodada=1, competidor1=inscricao_mock_1, competidor2=inscricao_mock_2)
    
    # Cria um competidor que não está na luta
    robo_intruso = Robo("Intruso", 1.0)
    competicao_intruso = CompeticaoCombate("Outra Competição", evento=None)
    vencedor_invalido = Inscricao(robo_intruso, competicao_intruso)

    # Act & Assert
    with pytest.raises(ValueError, match="Vencedor inválido para esta luta"):
        luta.registrar_resultado(vencedor_invalido)

def test_luta_estado_inicial_deve_ser_agendada(inscricao_mock_1, inscricao_mock_2):
    # Arrange & Act
    luta = Luta(rodada=1, competidor1=inscricao_mock_1, competidor2=inscricao_mock_2)
    
    # Assert
    assert luta.status == StatusLuta.AGENDADA
    assert luta.vencedor is None


def test_tomada_de_tempo_criacao_armazena_dados_corretamente():
    # Arrange
    tempo_esperado = 12.34
    
    # Act
    tomada = TomadaDeTempo(tempo_esperado)
    
    # Assert
    assert tomada.tempo_em_segundos == tempo_esperado
    assert isinstance(tomada.data_registro, datetime)