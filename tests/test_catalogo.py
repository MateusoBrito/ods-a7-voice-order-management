import sys
import os
import pytest

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modulo_catalogo.repository import CatalogoRepository

@pytest.fixture
def repo_catalogo():
    return CatalogoRepository(json_path="data/cardapio_mock.json")

def test_buscar_produto_existente_com_sucesso(repo_catalogo):
    produto = repo_catalogo.buscar_produto("X-Salada")
    assert produto is not None
    assert produto.nome == "X-Salada"
    assert produto.disponibilidade is True

def test_buscar_produto_case_insensitive(repo_catalogo):
    produto = repo_catalogo.buscar_produto("coca")
    assert produto is not None
    assert "Coca-Cola" in produto.nome

def test_buscar_produto_indisponivel(repo_catalogo):
    # Produto mockado no cardápio com disponibilidade = False
    produto = repo_catalogo.buscar_produto("vegetariano futuro")
    if produto:
        assert produto.disponibilidade is False

def test_buscar_produto_inexistente(repo_catalogo):
    produto = repo_catalogo.buscar_produto("Pizza de Calabresa")
    assert produto is None

def test_buscar_produto_com_fuzzy_matching(repo_catalogo):
    # Testa tolerância a pequenos erros do I5 (Task 18)
    produto = repo_catalogo.buscar_produto_com_fuzzy("x saladas")
    assert produto is not None
    assert produto.nome == "X-Salada"