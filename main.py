import json
from src.modulo_catalogo.repository import CatalogoRepository
from src.modulo_nlu.classifier import IntentClassifier
from src.modulo_nlu.subscriber import AudioEventSubscriber

def main():
    print("==================================================")
    print("--- Inicializando Módulo do Catálogo (A7 Varejo) ---")
    print("==================================================")
    
    # 1. Instanciação do Repositório de Catálogo
    catalogo = CatalogoRepository(json_path="data/cardapio_mock.json")

    # Teste Catálogo: Busca simples
    termo_busca = "coca"
    print(f"\n[TESTE CATÁLOGO] Entrada de busca: '{termo_busca}'")
    produto_coca = catalogo.buscar_produto(termo_busca)
    if produto_coca:
        print(f" -> Resultado: Encontrado '{produto_coca.nome}' | Preço: R$ {produto_coca.preco:.2f} | Disponível: {produto_coca.disponibilidade}")

    print("\n==================================================")
    print("--- Inicializando Módulo NLU (Ingestão + Slots) ---")
    print("==================================================")

    # 2. Instanciação do NLU (Classificador e Assinante do Barramento)
    classifier = IntentClassifier()
    subscriber = AudioEventSubscriber(classifier)

    # Lista de cenários para testar a NLU (NLU-1 e NLU-2)
    cenarios_teste = [
        {
            "descricao": "Critério de Aceite NLU-2 (Quantidade por extenso + Plural)",
            "payload": {"texto": "quero dois x-saladas", "confianca": 0.95}
        },
        {
            "descricao": "Quantidade Numérica + Produto com Nome Composto",
            "payload": {"texto": "me vê 2 coca-colas por favor", "confianca": 0.92}
        },
        {
            "descricao": "Intenção de Chamar Atendimento (Sem produtos)",
            "payload": {"texto": "pode chamar o garçom por gentileza", "confianca": 0.88}
        },
        {
            "descricao": "Filtro de Baixa Confiança de Áudio",
            "payload": {"texto": "quero um x salada", "confianca": 0.35}
        }
    ]

    for i, cenario in enumerate(cenarios_teste, start=1):
        print(f"\n[TESTE NLU {i}] {cenario['descricao']}")
        print(f" Entrada (I5/B3): {cenario['payload']}")
        
        resultado_nlu = subscriber.on_message_received(cenario['payload'])
        
        # Imprime o JSON retornado formatado
        print(" Saída do NLU:")
        print(json.dumps(resultado_nlu, indent=4, ensure_ascii=False))

    print("\n==================================================")
    print("--- Teste Integrado: NLU-2 (Slots) + Catálogo ---")
    print("==================================================")

    # Executa a frase de teste principal
    entrada_integrada = {"texto": "quero duas cocas", "confianca": 0.96}
    print(f"Entrada de Áudio Transcrito: '{entrada_integrada['texto']}'")
    
    # 1. Processa no NLU
    resultado_integrado = subscriber.on_message_received(entrada_integrada)
    print(f"1. NLU Processado -> Intenção: {resultado_integrado.get('intencao')}")
    print(f"   Slots Extraídos -> {resultado_integrado.get('entidades')}")

    # 2. Recupera o nome do produto extraído pelo NLU-2
    entidades = resultado_integrado.get("entidades", {})
    nome_produto_extraido = entidades.get("produto", "")
    qtd_extraida = entidades.get("quantidade", 1)

    # 3. Consulta no Catálogo usando o nome do produto extraído pelos slots
    produto_no_banco = catalogo.buscar_produto(nome_produto_extraido)

    if produto_no_banco:
        subtotal = produto_no_banco.preco * qtd_extraida
        print(f"2. Busca no Catálogo -> SUCESSO!")
        print(f"   - Item Mapeado: {produto_no_banco.nome}")
        print(f"   - Quantidade: {qtd_extraida}")
        print(f"   - Preço Unitário: R$ {produto_no_banco.preco:.2f}")
        print(f"   - Valor Total: R$ {subtotal:.2f}")
        print(f"   - Status no Estoque: {'Disponível' if produto_no_banco.disponibilidade else 'Indisponível'}")
    else:
        print(f"2. Busca no Catálogo -> Produto '{nome_produto_extraido}' não encontrado no cardápio.")

if __name__ == "__main__":
    main()