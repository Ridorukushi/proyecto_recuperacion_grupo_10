/** Interfaces que reflejan el contrato de la API (specs/001-catalogo-sitios/contracts/openapi.yaml). */

export interface Opcion {
  clave: string;
  etiqueta: string;
}

export interface PrecioReferencia {
  valor_cop: number;
  varios: boolean;
  fecha_referencia_precio: string;
}

export interface SitioResumen {
  slug: string;
  nombre: string;
  municipio: Opcion;
  categoria: Opcion;
  precio_referencia: PrecioReferencia | null;
}

export interface Precio {
  concepto: string;
  valor_cop: number;
}

export interface SitioDetalle {
  slug: string;
  nombre: string;
  municipio: Opcion;
  categoria: Opcion;
  descripcion: string | null;
  latitud: number;
  longitud: number;
  horario: string | null;
  como_llegar: string | null;
  precios: Precio[];
  fecha_referencia_precio: string | null;
  fuentes: string[];
}

export interface Filtros {
  municipios: Opcion[];
  categorias: Opcion[];
}

export interface FiltrosLista {
  municipio?: string;
  categoria?: string;
  q?: string;
  orden?: 'nombre' | 'precio';
}
