# Definição das estruturas de dados (Data Classes)

from dataclasses import dataclass, field
from typing import List

@dataclass
class Produto:
    id: int
    nome: str
    preco: float
    variacoes: List[str] = field(default_factory=list)
    disponibilidade: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "Produto":
        """Converte um dicionário JSON na classe Produto."""
        return cls(
            id=data["id"],
            nome=data["nome"],
            preco=float(data["preco"]),
            variacoes=data.get("variacoes", []),
            disponibilidade=bool(data.get("disponibilidade", True))
        )