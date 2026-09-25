# Simulação/Ingestão do evento do barramento (B3/I5)

import json
from typing import Dict, Any
from src.modulo_nlu.classifier import IntentClassifier

class AudioEventSubscriber:
    """
    Simula a Ingestão do Barramento (B3) recebendo eventos de transcrição do I5.
    """
    def __init__(self, classifier: IntentClassifier):
        self.classifier = classifier

    def on_message_received(self, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Garante a assinatura do contrato e processa o payload vindo do I5.
        Envelope esperado: {"texto": str, "confianca": float}
        """
        texto_transcrito = event_payload.get("texto", "")
        confianca = event_payload.get("confianca", 0.0)

        # Regra de corte para baixas confianças de áudio (I5)
        if confianca < 0.5:
            return {
                "intencao": "INDETERMINADO",
                "texto_bruto": texto_transcrito,
                "erro": "Confiança do áudio muito baixa"
            }

        # Processa e classifica a intenção
        return self.classifier.classify(texto_transcrito)