# Modelo de datos: 002-ordenar-por-precio

Esta spec **no cambia** las tablas ni los archivos de datos de la spec 001
([../001-catalogo-sitios/data-model.md](../001-catalogo-sitios/data-model.md)).

## Valor nuevo (no se guarda)

| Concepto | Valores | Predeterminado | Dónde vive |
|---|---|---|---|
| `orden` | `nombre`, `precio` | `nombre` | Parámetro de consulta de `GET /api/sitios` y de la URL de la lista |

## Regla de orden por precio
Clave de orden, de izquierda a derecha:
1. Sitios con precio de referencia conocido primero; sin precio al final.
2. Precio de referencia (`precio_referencia.valor_cop`, el menor precio conocido) de menor a mayor; 0 va primero.
3. Nombre normalizado (`sitio.nombre_normalizado`) para desempatar y para ordenar los sitios sin precio.
