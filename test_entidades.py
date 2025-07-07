
import pytest
from esqueleto import Equipe, Membro, Robo, LiderDeEquipe

@pytest.fixture
def lider_stub():
    return LiderDeEquipe("Líder Stub", "lider@stub.com", "stub")

def test_equipe_criacao_armazena_lider_e_listas_vazias(lider_stub):
    # Arrange
    nome_equipe = "Equipe de Teste"
    
    # Act
    equipe = Equipe(nome_equipe, lider_stub)
    
    # Assert
    assert equipe.nome == nome_equipe
    assert equipe.lider == lider_stub
    assert equipe.membros == []
    assert equipe.robos == []

def test_membro_criacao_armazena_dados_corretamente():
    # Arrange
    nome_membro = "João"
    funcao_membro = "Piloto"
    
    # Act
    membro = Membro(nome_membro, funcao_membro)
    
    # Assert
    assert membro.nome == nome_membro
    assert membro.funcao == funcao_membro

def test_robo_criacao_armazena_dados_e_disponivel_e_true():
    # Arrange
    nome_robo = "Centurion"
    peso_robo = 3.0
    
    # Act
    robo = Robo(nome_robo, peso_robo)
    
    # Assert
    assert robo.nome == nome_robo
    assert robo.peso == peso_robo
    assert robo.disponivel is True