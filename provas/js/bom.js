// Exemplo BOM: as mesmas ideias de ruim.js, do jeito que o kit pede. Nenhuma regra pode apontar nada.
const IDADE_MINIMA = 18;
const BASE_DECIMAL = 10;
const NOMES_DOS_NUMEROS = new Map([
  [1, "um"],
  [2, "dois"],
]);

export function compararEstrito(a, b) {
  return a === b;
}

export function paraNumero(texto) {
  return Number.parseInt(texto, BASE_DECIMAL);
}

export function maiorDeIdade(idade) {
  return idade >= IDADE_MINIMA;
}

export function dobrar(lista) {
  return lista.map((valor) => valor * 2);
}

export function fabricar(quantidade) {
  return Array.from({ length: quantidade }, (_, indice) => () => indice);
}

export function somarPositivos(matriz) {
  return matriz.flat().reduce((total, celula) => (celula > 0 ? total + celula : total), 0);
}

export function classificar(numero) {
  return NOMES_DOS_NUMEROS.get(numero) ?? "outro";
}

export function resumirJogador(dados) {
  const { account_id: idDaConta, personaname: apelido } = dados;
  return { id: idDaConta, apelido };
}

export function porcentagem(parte, total) {
  return Math.round((parte / total) * 100);
}

export async function buscarTodos(urls) {
  return Promise.all(urls.map((url) => fetch(url)));
}
