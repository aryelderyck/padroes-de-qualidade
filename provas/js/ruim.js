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

export function igualASiMesmo(x) {
  return x === x;
}

export function depoisDoRetorno() {
  return 1;
  console.log("nunca roda");
}

export function condicaoFixa() {
  if (true) {
    return "sempre";
  }
  return "nunca";
}

export function lacoSemFim(fazer) {
  let pronto = false;
  while (!pronto) {
    fazer();
  }
}

export function ehInvalido(x) {
  return x === NaN;
}

export function ehTexto(x) {
  return typeof x === "strnig";
}

export function cair(x) {
  let nome = "";
  switch (x) {
    case 1:
      nome = "um";
    case 2:
      nome = "dois";
      break;
    default:
      nome = "outro";
  }
  return nome;
}

export function promessaComRetorno() {
  return new Promise((resolver) => resolver);
}

export function sombra(valor) {
  const lista = [valor];
  return lista.map((valor) => valor);
}

export function coagir(x) {
  return !!x;
}

export function retornoIrregular(x) {
  if (x) {
    return 1;
  }
}

export function lancarTexto() {
  throw "deu errado";
}

export function rejeitarTexto() {
  return Promise.reject("deu errado");
}

export function saudacao(nome) {
  return "Olá, ${nome}";
}

export async function umPorVez(urls) {
  const respostas = [];
  for (const url of urls) {
    respostas.push(await fetch(url));
  }
  return respostas;
}

export function agendar() {
  globalThis.setTimeout("alert('oi')", 100);
}

export function criarFuncao() {
  return new Function("a", "return a");
}

export const LINK = "javascript:void(0)";

export function callbacks(a) {
  a(() => {
    a(() => {
      a(() => {
        a(() => {});
      });
    });
  });
}

export function ifSozinho(a, b) {
  if (a) {
    return 1;
  } else {
    if (b) {
      return 2;
    }
  }
  return 0;
}

export function ternarios(a, b) {
  const aninhado = a ? 1 : b ? 2 : 0;
  const inutil = a ? true : false;
  return [aninhado, inutil];
}

export function retornoInutil(a) {
  a();
  return;
}

export function longa(total) {
  let soma = total;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  soma += 1;
  return soma;
}
