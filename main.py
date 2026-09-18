from src.modulo_catalogo.repository import CatalogoRepository

def main():
    print("--- Inicializando Módulo do Catálogo (A7 Varejo) ---")
    
    # Instancia o repositório lendo os dados mockados
    catalogo = CatalogoRepository(json_path="data/cardapio_mock.json")

    # Teste 1: Busca existente
    termo = "coca"
    produto = catalogo.buscar_produto(termo)
    
    if produto:
        print(f"\n[SUCESSO] Produto encontrado para '{termo}':")
        print(f" - Nome: {produto.nome}")
        print(f" - Preço: R$ {produto.preco:.2f}")
        print(f" - Variações: {', '.join(produto.variacoes)}")
        print(f" - Disponível: {'Sim' if produto.disponibilidade else 'Não'}")
    else:
        print(f"\n[FALHA] Produto '{termo}' não encontrado.")

    # Teste 2: Produto indisponível
    termo_indisponivel = "x-burguer"
    produto_ind = catalogo.buscar_produto(termo_indisponivel)
    if produto_ind:
        print(f"\n[SUCESSO] Produto encontrado para '{termo_indisponivel}':")
        print(f" - Nome: {produto_ind.nome}")
        print(f" - Disponível: {'Sim' if produto_ind.disponibilidade else 'Não'}")

if __name__ == "__main__":
    main()