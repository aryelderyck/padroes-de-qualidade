# Exemplo RUIM de propósito: cada trecho precisa ser apontado por uma regra do kit.
# Não copie nada daqui. A lista do que deve ser pego está em provas/conferir-provas.py.
import datetime

import requests


def buscarUsuario(conexao, nome):
  cursor = conexao.cursor()
  cursor.execute(f"SELECT * FROM usuarios WHERE nome = '{nome}'")
  return cursor.fetchall()


def acumular(item, lista=[]):
    lista.append(item)
    return lista


def agora():
    return datetime.datetime.now()


def maior_de_idade(idade):
    return idade > 18


def muitos_parametros(a, b, c, d, e, f, g):
    return a + b + c + d + e + f + g


def classificar(n):
    if n == 1:
        return "um"
    elif n == 2:
        return "dois"
    elif n == 3:
        return "três"
    elif n == 4:
        return "quatro"
    elif n == 5:
        return "cinco"
    elif n == 6:
        return "seis"
    elif n == 7:
        return "sete"
    elif n == 8:
        return "oito"
    elif n == 9:
        return "nove"
    elif n == 10:
        return "dez"
    elif n == 11:
        return "onze"
    return "outro"


def engolir():
    try:
        return int("x")
    except:
        pass


def depurar(valor):
    print(valor)
    sobra = 1
    if valor == None:
        return 0
    return 1


def baixar(url):
    return requests.get(url)


def esconder():
    list = [1, 2]
    return list


def fabricar():
    funcoes = []
    for i in range(3):
        funcoes.append(lambda: i)
    return funcoes


def aninhado(matriz):
    total = 0
    for linha in matriz:
        for celula in linha:
            if celula:
                if celula > 0:
                    total += celula
    return total


# total = aninhado(matriz) + 1


def sem_uso(a, b):
    return a


def comparar_texto(valor):
    return valor is "sim"


def normalizar(nomes):
    for nome in nomes:
        nome = nome.strip()
        print(nome)


class Carrinho:
    itens = []


def longa(total):
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    total += 1
    return total
