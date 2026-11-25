# Investigación (Fase 0): 002-ordenar-por-precio

## D1. Dónde se ordena
- **Decisión:** en el backend, dentro de `GET /api/sitios`, con un parámetro nuevo `orden` (`nombre` |
  `precio`, por defecto `nombre`). El orden por precio se aplica en Python sobre la lista ya filtrada, con la clave
  `(sin precio, precio de referencia, nombre normalizado)`.
- **Razón:** el precio de referencia (el menor precio conocido) ya se calcula en Python para cada sitio; el
  catálogo tiene 10 a 15 sitios, así que ordenar en memoria es simple y suficiente (YAGNI). El frontend no
  reordena: muestra lo que devuelve la API, como en la spec 001.
- **Alternativas:** ordenar en SQL con una subconsulta `MIN(valor_cop)` (más compleja sin beneficio con 15
  sitios); ordenar en el frontend (duplicaría la regla y no serviría a otros clientes de la API).

## D2. Validación del parámetro
- **Decisión:** si `orden` no es `nombre` ni `precio`, la API responde 422 con
  `{"detalle": "El orden «<valor>» no es válido. Usa «nombre» o «precio»."}`. Un valor de más de 60 caracteres no se
  repite en el mensaje (misma regla S2 de la spec 001).

## D3. Frontend
- **Decisión:** un `<select id="orden">` con etiqueta «Ordenar por» y opciones `nombre` → «Nombre (A–Z)» y
  `precio` → «Precio (de menor a mayor)». El valor vive en un signal, se envía como `orden` solo cuando es `precio`
  y se guarda en los parámetros de la URL junto a los filtros. «Limpiar filtros» lo devuelve a `nombre`.

## D4. Sin cambios de datos
- No cambia el esquema de la base ni el formato de los archivos de datos.
