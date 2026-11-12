// Exemplo BOM para as regras que dependem de tipo. Nenhuma regra pode apontar nada.
export type Forma = "circulo" | "quadrado";

const LADOS_DO_QUADRADO = 4;

export function lados(forma: Forma): number {
  switch (forma) {
    case "circulo":
      return 0;
    case "quadrado":
      return LADOS_DO_QUADRADO;
  }
}

export function paraTexto(valor: number): string {
  return String(valor);
}

async function gravar(): Promise<void> {
  await Promise.resolve();
}

export async function esperar(): Promise<void> {
  await gravar();
}

export function resumirJogador(dados: { account_id: number; personaname: string }): {
  id: number;
  apelido: string;
} {
  const { account_id: idDaConta, personaname: apelido } = dados;
  return { id: idDaConta, apelido };
}
