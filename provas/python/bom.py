"""Exemplo BOM: as mesmas ideias de ruim.py, do jeito que o kit pede.

Nenhuma regra pode apontar nada aqui.
"""

import sqlite3
from datetime import UTC, datetime

IDADE_MINIMA = 18
NOMES_DOS_NUMEROS = {1: "um", 2: "dois", 3: "três"}


def buscar_usuario(conexao: sqlite3.Connection, nome: str) -> list[tuple[int, str]]:
    cursor = conexao.execute("SELECT id, nome FROM usuarios WHERE nome = ?", (nome,))
    return cursor.fetchall()


def acumular(item: int, lista: list[int] | None = None) -> list[int]:
    resultado = [] if lista is None else list(lista)
    resultado.append(item)
    return resultado


def agora() -> datetime:
    return datetime.now(tz=UTC)


def maior_de_idade(idade: int) -> bool:
    return idade >= IDADE_MINIMA


def classificar(numero: int) -> str:
    return NOMES_DOS_NUMEROS.get(numero, "outro")


def converter(texto: str) -> int | None:
    try:
        return int(texto)
    except ValueError:
        return None


def somar_positivos(matriz: list[list[int]]) -> int:
    return sum(celula for linha in matriz for celula in linha if celula > 0)
