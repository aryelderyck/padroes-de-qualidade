"""Código que funciona e que só o modo completo acusa (número mágico, print, parâmetros demais).

No modo essencial precisa passar sem nenhum apontamento.
"""


def preco_final(preco, cupom, frete, taxa, desconto, bonus):
    if cupom and preco > 250:
        return preco * 0.9 + frete
    print(taxa, desconto, bonus)
    return preco + 3.5
