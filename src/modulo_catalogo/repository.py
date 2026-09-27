# Classe que lê o JSON e faz a busca textual/fuzzy

import json
import os
from difflib import get_close_matches
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
        if not termo_limpo:
            return None
            
        for produto in self.produtos:
            if termo_limpo in produto.nome.lower():
                return produto
                
        return None

    def buscar_produto_com_fuzzy(self, nome_busca: str, cutoff: float = 0.5) -> Optional[Produto]:
        """
        Atende à Task 18: Busca o produto aceitando pequenos erros de transcrição (Fuzzy Matching).
        """
        termo_limpo = nome_busca.strip().lower()
        if not termo_limpo:
            return None

        # 1. Tenta a busca por substring simples primeiro
        produto_exato = self.buscar_produto(termo_limpo)
        if produto_exato:
            return produto_exato

        # 2. Se não encontrou, aplica similaridade textual (difflib)
        mapa_nomes = {p.nome.lower(): p for p in self.produtos}
        matches = get_close_matches(termo_limpo, list(mapa_nomes.keys()), n=1, cutoff=cutoff)

        if matches:
            return mapa_nomes[matches[0]]

        return None