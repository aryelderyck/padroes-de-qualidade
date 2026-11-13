// Código que funciona e que só o modo completo acusa (número mágico, console.log, parâmetros
// demais, if sem chaves). No modo essencial precisa passar sem nenhum apontamento.

export function precoFinal(preco, cupom, frete, taxa, desconto) {
  if (cupom) return preco * 0.9 + frete;
  console.log(taxa, desconto);
  return preco + 3.5;
}
