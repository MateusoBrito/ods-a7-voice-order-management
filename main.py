import json
from src.modulo_catalogo.repository import CatalogoRepository
from src.modulo_nlu.classifier import IntentClassifier
from src.modulo_nlu.subscriber import AudioEventSubscriber

def main():
    print("==================================================")
    print("--- Inicializando Módulo A7 (Varejo) ---")
    print("==================================================")
    
    # 1. Instancia o Catálogo (Task 16)
    catalogo = CatalogoRepository(json_path="data/cardapio_mock.json")

    # 2. Instancia o NLU injetando o catálogo para resolução de IDs (Tasks 17 e 18)
    classifier = IntentClassifier(catalogo_repo=catalogo)
    subscriber = AudioEventSubscriber(classifier)

    # 3. Teste do Critério de Aceite da Task 18 ("quero dois x-saladas")
    evento_teste_18 = {
        "texto": "quero dois x-saladas",
        "confianca": 0.95
    }

    print(f"\n[ENTRADA SIMULADA (I5/B3)]: {evento_teste_18}")
    resultado = subscriber.on_message_received(evento_teste_18)

    print("\n[SAÍDA DO MOTOR NLU]:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()