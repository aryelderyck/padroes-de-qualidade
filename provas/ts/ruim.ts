// Exemplo RUIM de propósito, para as regras que dependem de tipo. Não copie nada daqui.
export type Forma = "circulo" | "quadrado";

export function lados(forma: Forma): number {
  switch (forma) {
    case "circulo":
      return 0;
  }
  return 4;
}

export function paraTexto(valor: any): string {
  return String(valor);
}

async function gravar(): Promise<void> {
  await Promise.resolve();
}

export function esquecerDeEsperar(): void {
  gravar();
}

export function compararFrouxo(a: number, b: number): boolean {
  return a == b;
}

export function agendar(): void {
  setTimeout("alert('oi')", 100);
}
