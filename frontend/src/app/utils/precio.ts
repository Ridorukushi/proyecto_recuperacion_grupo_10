import { PrecioReferencia } from '../models/sitio';

const MESES = ['ene.', 'feb.', 'mar.', 'abr.', 'may.', 'jun.', 'jul.', 'ago.', 'sept.', 'oct.', 'nov.', 'dic.'];

const NO_DISPONIBLE = 'Precio no disponible';

/** Separador de miles con punto, puesto en código para no depender de `Intl`. */
function conMiles(valor: number): string {
  return String(valor).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

/** Mes y año de una fecha `AAAA-MM-DD`, leídos del texto para evitar cambios por zona horaria. */
function mesYAnio(fecha: string): string {
  const [anio, mes] = fecha.split('-');
  return `${MESES[Number(mes) - 1]} ${anio}`;
}

/** Precio de un concepto: `$25.000 COP (aprox., consultado en nov. 2026)`, `Gratis` o `Precio no disponible`. */
export function formatearPrecio(valorCop: number | null, fecha: string | null): string {
  if (valorCop === null) return NO_DISPONIBLE;
  if (valorCop === 0) return 'Gratis';
  const consulta = fecha ? ` (aprox., consultado en ${mesYAnio(fecha)})` : ' (aprox.)';
  return `$${conMiles(valorCop)} COP${consulta}`;
}

/** Precio de referencia de la lista: antepone «Desde» si hay varios precios conocidos. */
export function formatearPrecioReferencia(referencia: PrecioReferencia | null): string {
  if (referencia === null) return NO_DISPONIBLE;
  if (referencia.valor_cop === 0) return referencia.varios ? 'Gratis (hay otras tarifas)' : 'Gratis';
  const texto = formatearPrecio(referencia.valor_cop, referencia.fecha_referencia_precio);
  return referencia.varios ? `Desde ${texto}` : texto;
}
