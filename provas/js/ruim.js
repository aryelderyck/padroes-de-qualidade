// Exemplo RUIM de propósito: cada trecho precisa ser apontado por uma regra do kit.
// Não copie nada daqui. A lista do que deve ser pego está em provas/conferir-provas.py.
var contador = 0;

export function compararFrouxo(a, b) {
    if (a == b) {
        return true;
    } else {
        return false;
    }
}

export function executar(codigo) {
  return eval(codigo);
}

export function paraNumero(texto) {
  return parseInt(texto);
}

export function maiorDeIdade(idade) {
  return idade > 18;
}

export function muitos(a, b, c, d, e) {
  return a + b + c + d + e;
}

export function dobrar(lista) {
  return lista.map((x) => {
    x * 2;
  });
}

export function fabricar() {
  const funcoes = [];
  for (var i = 0; i < 3; i++) {
    funcoes.push(function () {
      return i;
    });
  }
  return funcoes;
}

export function profundo(matriz) {
  let total = 0;
  for (const linha of matriz) {
    for (const celula of linha) {
      if (celula) {
        if (celula > 0) {
          total += celula;
        }
      }
    }
  }
  return total;
}

export function reatribuir(valor) {
  valor = valor + 1;
  let fixo = 10;
  return valor + fixo;
}

export function classificar(n) {
  if (n === 1) return "um";
  if (n === 2) return "dois";
  if (n === 3) return "três";
  if (n === 4) return "quatro";
  if (n === 5) return "cinco";
  if (n === 6) return "seis";
  if (n === 7) return "sete";
  if (n === 8) return "oito";
  if (n === 9) return "nove";
  if (n === 10) return "dez";
  if (n === 11) return "onze";
  return "outro";
}

export function semUso() {
  const sobra = 1;
}

export function tipo(x) {
  switch (x) {
    case 1:
      return "um";
  }
  return "outro";
}

export const nome_errado = contador;
