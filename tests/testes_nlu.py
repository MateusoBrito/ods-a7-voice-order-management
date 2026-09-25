import sys
import os

import pytest

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modulo_nlu.classifier import IntentClassifier
from src.modulo_nlu.subscriber import AudioEventSubscriber

@pytest.fixture
def nlu_pipeline():
    classifier = IntentClassifier()
    subscriber = AudioEventSubscriber(classifier)
    return subscriber

def test_criterio_de_aceite_nlu1(nlu_pipeline):
    # Evento simulado do componente i5 via barramento
    evento_i5 = {
        "texto": "quero dois x-saladas",
        "confianca": 0.95
    }

    resultado = nlu_pipeline.on_message_received(evento_i5)

    assert resultado["intencao"] == "ADICIONAR_ITEM"
    assert resultado["texto_bruto"] == "dois x-saladas"
    print("Resultado do teste de critério de aceite NLU1:", resultado)

def test_variacao_verbos_adicionar(nlu_pipeline):
    evento = {"texto": "me vê uma coca cola por favor", "confianca": 0.90}
    resultado = nlu_pipeline.on_message_received(evento)

    assert resultado["intencao"] == "ADICIONAR_ITEM"
    assert resultado["texto_bruto"] == "uma coca cola"
    print("Resultado do teste de variação de verbos para adicionar:", resultado)

def test_intencao_chamar_atendimento(nlu_pipeline):
    evento = {"texto": "pode chamar o garçom", "confianca": 0.88}
    resultado = nlu_pipeline.on_message_received(evento)
    print("Resultado do teste de intenção chamar atendimento:", resultado)

    assert resultado["intencao"] == "CHAMAR_ATENDIMENTO"