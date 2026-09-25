#Lidar com extração de slots (quantidade e produto) do texto limpo do NLU

import re
from typing import Dict, Any

class SlotExtractor:
    def __init__(self):
        # Mapeamento de números por extenso simples
        self.numeros_extenso = {
            "um": 1, "uma": 1,
            "dois": 2, "duas": 2,
            "três": 3, "tres": 3,
            "quatro": 4, "cinco": 5
        }

    def extract_slots(self, texto_bruto: str) -> Dict[str, Any]:
        """
        Extrai quantidade e o nome limpo do produto a partir do texto bruto.
        """
        texto = texto_bruto.strip().lower()
        quantidade = 1  # Quantidade padrão se não informada
        
        # 1. Tenta extrair quantidade numérica (ex: "2 x-saladas")
        match_num = re.search(r"\b(\d+)\b", texto)
        if match_num:
            quantidade = int(match_num.group(1))
            texto = re.sub(r"\b\d+\b", "", texto).strip()
        else:
            # 2. Tenta extrair quantidade por extenso (ex: "dois x-saladas")
            for palavra, valor in self.numeros_extenso.items():
                if re.search(rf"\b{palavra}\b", texto):
                    quantidade = valor
                    texto = re.sub(rf"\b{palavra}\b", "", texto).strip()
                    break

        # 3. Trata plural básico do produto (ex: "x-saladas" -> "x-salada")
        produto_limpo = texto.strip()
        if produto_limpo.endswith("s") and not produto_limpo.endswith("is"):
            # Remove o 's' do plural simples para facilitar o match no catálogo
            produto_limpo = produto_limpo[:-1]

        return {
            "produto": produto_limpo,
            "quantidade": quantidade,
            "variacoes": []
        }