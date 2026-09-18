# Classe que lê o JSON e faz a busca textual

import json
import os
from typing import Optional, List
from src.modulo_catalogo.models import Produto

class CatalogoRepository:
    def __init__(self, json_path: str = "data/cardapio_mock.json"):
        self.json_path = json_path
        self.produtos: List[Produto] = []
        self._carregar_dados()

    def _carregar_dados(self):
        """Lê o arquivo JSON mockado do disco."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Arquivo de catálogo não encontrado: {self.json_path}")
            
        with open(self.json_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
            self.produtos = [Produto.from_dict(item) for item in dados]

    def buscar_produto(self, nome_busca: str) -> Optional[Produto]:
        """
        Simula consulta textual rápida por substring (estilo ILIKE).
        Retorna o primeiro produto que contiver o termo pesquisado (insensível a maiúsculas/minúsculas).
        """
        termo_limpo = nome_busca.strip().lower()
        
        for produto in self.produtos:
            if termo_limpo in produto.nome.lower():
                return produto
                
        return None