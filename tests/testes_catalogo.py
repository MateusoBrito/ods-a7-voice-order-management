from src.modulo_catalogo.repository import CatalogoRepository
import pytest

@pytest.fixture
def repo_catalogo():
    return CatalogoRepository(json_path="data/cardapio_mock.json")

def test_buscar_produto_existente_com_sucesso(repo_catalogo):
    produto = repo_catalogo.buscar_produto("X-Salada")
    assert produto is not None
    assert produto.nome == "X-Salada"
    assert produto.preco == 18.50
    assert produto.disponibilidade is True

def test_buscar_produto_case_insensitive(repo_catalogo):
    # Deve encontrar "Coca-Cola" mesmo digitando "coca" em minúsculas
    produto = repo_catalogo.buscar_produto("coca")
    assert produto is not None
    assert produto.nome == "Coca-Cola"

def test_buscar_produto_indisponivel(repo_catalogo):
    produto = repo_catalogo.buscar_produto("x-burguer")
    assert produto is not None
    assert produto.disponibilidade is False

def test_buscar_produto_inexistente(repo_catalogo):
    produto = repo_catalogo.buscar_produto("Pizza de Calabresa")
    assert produto is None