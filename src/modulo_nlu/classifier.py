import re
from typing import Dict, Any
from src.modulo_nlu.slot_extractor import SlotExtractor

class IntentClassifier:
    def __init__(self):
        self.slot_extractor = SlotExtractor()
        self.rules = [
            (r"\b(quero|me vê|me ve|vou pedir|adiciona|adicionar|traz|pede)\b", "ADICIONAR_ITEM"),
            (r"\b(chama|chamada|atendente|garçom|garcom|ajuda)\b", "CHAMAR_ATENDIMENTO"),
            (r"\b(conta|fechar|pagamento|pagar|nota)\b", "PEDIR_CONTA")
        ]
        self.stopwords_regex = r"\b(quero|me|vê|ve|vou|pedir|adiciona|adicionar|traz|pede|por|favor|gostaria|de)\b"

    def classify(self, text: str) -> Dict[str, Any]:
        text_clean = text.strip()
        text_lower = text_clean.lower()
        intent = "DESCONHECIDO"

        for pattern, mapped_intent in self.rules:
            if re.search(pattern, text_lower):
                intent = mapped_intent
                break

        clean_product_text = re.sub(self.stopwords_regex, "", text_lower, flags=re.IGNORECASE)
        clean_product_text = re.sub(r"\s+", " ", clean_product_text).strip()

        # Extrai os slots de produto e quantidade (NLU-2 / SCRUM-17)
        slots = self.slot_extractor.extract_slots(clean_product_text)

        return {
            "intencao": intent,
            "texto_bruto": clean_product_text,
            "entidades": slots
        }