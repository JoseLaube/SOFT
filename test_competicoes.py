import pytest
from esqueleto import (
    CompeticaoCombate, CompeticaoSeguidorDeLinha, Evento, Robo, Inscricao, 
    StatusInscricao, Resultado, TomadaDeTempo
)

@pytest.fixture
def evento_vazio():
    org_stub = type('Organizador', (), {})()
    return Evento("Evento de Teste", "2024-01-01", "2024-01-02", org_stub)




def test_gerar_estrutura_combate_sem_inscricoes_aprovadas(evento_vazio):
    # Arrange
    comp_combate = CompeticaoCombate("Combate Vazio", evento_vazio)
    robo1 = Robo("Robo Pendente", 1.0)
    robo2 = Robo("Robo Reprovado", 1.0)
    
    insc1 = Inscricao(robo1, comp_combate)
    insc1.status = StatusInscricao.PENDENTE
    
    insc2 = Inscricao(robo2, comp_combate)
    insc2.status = StatusInscricao.REPROVADA
    
    comp_combate.receber_inscricao(insc1)
    comp_combate.receber_inscricao(insc2)
    
    # Act
    comp_combate.gerar_estrutura() # Espera-se que crie uma chave com 0 robôs
    
    # Assert
    assert comp_combate.chave_batalha is not None
    assert len(comp_combate.chave_batalha.robos_participantes) == 0


def test_gerar_classificacao_sem_inscricoes(evento_vazio):
    # Arrange
    comp_seguidor = CompeticaoSeguidorDeLinha("Seguidor Vazio", evento_vazio)
    
    # Act
    classificacao = comp_seguidor.gerar_classificacao()
    
    # Assert
    assert classificacao == []

def test_inscricao_get_melhor_tempo_com_lista_vazia():
    # Arrange
    robo_stub = Robo("Robo Sem Tempo", 0.5)
    comp_stub = CompeticaoSeguidorDeLinha("Pista de Teste", evento_vazio)
    inscricao = Inscricao(robo_stub, comp_stub)
    
    # Act
    melhor_tempo = inscricao.get_melhor_tempo()
    
    # Assert
    assert melhor_tempo is None