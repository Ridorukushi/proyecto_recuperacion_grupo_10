# Modelo de datos: 001-catalogo-sitios

Esquema en `backend/db/001_esquema.sql` (PostgreSQL 16). Las reglas de validación se aplican al cargar
(Pydantic en `backend/app/carga.py`) y las restricciones de la base son la segunda barrera.

## Tablas

### `municipio`
| Campo | Tipo | Reglas |
|---|---|---|
| `clave` | `text` PK | sin tildes, minúsculas, guiones (`garzon`, `la-plata`) |
| `nombre` | `text` único, no nulo | etiqueta para mostrar (`Garzón`) |

Lista fija de los 37 municipios del Huila, cargada desde `backend/datos/municipios.json`.

### `sitio`
| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `integer` PK (identidad) | interno, no se expone |
| `slug` | `text` único, no nulo | derivado del nombre (D6), `^[a-z0-9-]{1,120}$` |
| `nombre` | `text` único, no nulo | 1–120 caracteres |
| `nombre_normalizado` | `text` no nulo | `normalizar(nombre)`; búsqueda y orden |
| `municipio_clave` | `text` FK → `municipio.clave`, no nulo | |
| `categoria` | `text` no nulo | `CHECK` en las 7 claves |
| `descripcion` | `text` nulo | ≤ 400 caracteres |
| `latitud` | `numeric(8,5)` no nulo | `CHECK 1.5 ≤ latitud ≤ 3.9` |
| `longitud` | `numeric(8,5)` no nulo | `CHECK -76.6 ≤ longitud ≤ -74.4` |
| `horario` | `text` nulo | nulo = «No disponible» |
| `como_llegar` | `text` nulo | nulo = «No disponible» |
| `fecha_referencia_precio` | `date` nulo | obligatoria si el sitio tiene precios |

### `precio`
| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `integer` PK | |
| `sitio_id` | `integer` FK → `sitio.id` `ON DELETE CASCADE` | |
| `concepto` | `text` no nulo | 1–80 caracteres (p. ej. «Entrada adulto») |
| `valor_cop` | `integer` no nulo | `CHECK valor_cop >= 0`; 0 = gratis |

Un precio desconocido **no se guarda** (no hay filas con valor nulo).

### `fuente`
| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `integer` PK | |
| `sitio_id` | `integer` FK → `sitio.id` `ON DELETE CASCADE` | |
| `url` | `text` no nulo | `http://` o `https://` |

Cada sitio tiene ≥ 1 fuente (se valida al cargar).

## Categorías (fijas en el código)
| Clave | Etiqueta |
|---|---|
| `arqueologia` | Arqueología |
| `naturaleza` | Naturaleza |
| `aventura` | Aventura |
| `cultura` | Cultura |
| `religioso` | Religioso |
| `gastronomia` | Gastronomía |
| `termales` | Termales |

## Formato de los archivos de datos

`backend/datos/sitios.json`: lista de fichas. Reemplaza el formato de la skill `datos-turisticos`
(se quita `aproximado`, `municipio` pasa a clave y `valor_cop` puede faltar o ser `null` si es desconocido).

```json
{
  "nombre": "…",
  "municipio": "villavieja",
  "categoria": "naturaleza",
  "descripcion": "…",
  "latitud": 3.2,
  "longitud": -75.1,
  "precios": [{ "concepto": "Entrada adulto", "valor_cop": null }],
  "fecha_referencia_precio": "2026-11-24",
  "horario": null,
  "como_llegar": null,
  "fuentes": ["https://…"]
}
```

`backend/datos/municipios.json`: `{"fuente": "https://…", "municipios": [{"clave": "neiva", "nombre": "Neiva"}, …]}`.

## Reglas de rechazo al cargar (CA-17 a CA-19)
1. Falta `nombre`, `municipio`, `categoria`, `latitud`, `longitud` o `fuentes` vacío; `nombre` de más de 120
   caracteres.
2. `municipio` no está entre las 37 claves; `categoria` no está entre las 7.
3. Coordenadas fuera de los bordes (inclusivos).
4. `valor_cop` negativo o no entero.
5. Hay al menos un precio conocido y falta `fecha_referencia_precio` (formato `AAAA-MM-DD`).
6. Dos fichas con el mismo `nombre` o el mismo `slug`.
7. `fuentes` con una URL que no empieza por `http://` o `https://`; `descripcion` > 400 caracteres;
   `concepto` de un precio vacío o > 80 caracteres.
8. `horario` > 200 caracteres, `como_llegar` > 500 caracteres o una URL de `fuentes` > 500 caracteres
   (hallazgo S4 de la revisión).
9. `nombre` sin ninguna letra ni dígito: produciría un `slug` vacío (hallazgo R3).

Si una ficha falla, no se guarda ninguna. Los mensajes de `ErrorCarga` están en español e incluyen el nombre del
campo (hallazgo R2). La recarga completa (`python -m app.carga`) valida todo **antes** de tocar la base y hace el
borrado y la carga en una sola transacción: si algo falla, el catálogo anterior queda intacto (hallazgo R1).
`001_esquema.sql` no borra tablas; el borrado solo ocurre en la recarga y en las pruebas, y las pruebas se niegan a
correr si el nombre de la base no contiene «prueba» (hallazgos S3 y R6).

## Estados
Sin transiciones: el catálogo es de solo lectura y se recarga completo.
