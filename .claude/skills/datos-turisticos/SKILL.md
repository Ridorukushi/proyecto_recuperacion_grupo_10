---
name: datos-turisticos
description: Formato y reglas de validación de una ficha de sitio turístico del Huila (precios COP aproximados, coordenadas, fuentes). Úsala al crear, importar, validar o mostrar datos del catálogo.
---

# Ficha de sitio turístico del Huila

Formato de `backend/datos/sitios.json`. El modelo canónico es
`specs/001-catalogo-sitios/data-model.md`: si cambia, se actualiza esta skill.

```json
{
  "nombre": "Nombre oficial del sitio",
  "municipio": "villavieja",
  "categoria": "naturaleza",
  "descripcion": "Texto propio y breve (máx. 400 caracteres).",
  "latitud": 3.2,
  "longitud": -75.1,
  "precios": [
    { "concepto": "Entrada adulto", "valor_cop": null }
  ],
  "fecha_referencia_precio": "2026-11-24",
  "horario": null,
  "como_llegar": null,
  "fuentes": ["https://..."]
}
```

Los valores del ejemplo son ilustrativos; no usarlos como datos reales.

## Reglas de validación
- Obligatorios: `nombre` (máx. 120 caracteres, único), `municipio`, `categoria`, `latitud`, `longitud` y al menos
  una URL `http(s)` en `fuentes`.
- `municipio`: la **clave** (sin tildes, minúsculas, guiones) de uno de los 37 municipios de
  `backend/datos/municipios.json`, p. ej. `garzon`, `la-plata`.
- `categoria`: `arqueologia`, `naturaleza`, `aventura`, `cultura`, `religioso`, `gastronomia` o `termales`.
- Coordenadas dentro del Huila, bordes incluidos: latitud 1.5 a 3.9 y longitud −76.6 a −74.4.
- `precios[].concepto`: 1 a 80 caracteres. `precios[].valor_cop`: entero ≥ 0; `0` = gratis; `null` = desconocido
  (no se guarda).
- Si queda al menos un precio conocido, `fecha_referencia_precio` es obligatoria (AAAA-MM-DD).
- `descripcion`, `horario` y `como_llegar` son opcionales: si no se conocen, van en `null`. Nunca se rellenan con
  suposiciones ni se copian textos de otros sitios web.

## Cómo se muestra al usuario
- Precio conocido: `$25.000 COP (aprox., consultado en nov. 2026)`. Meses: ene., feb., mar., abr., may., jun.,
  jul., ago., sept., oct., nov., dic.
- Gratis: «Gratis». Sin precio conocido: «Precio no disponible», nunca «$0».
- En la lista, con varios precios: «Desde » + el menor; si el menor es 0, «Gratis (hay otras tarifas)».
- Horario o cómo llegar desconocidos: «No disponible».
- Siempre mostrar el enlace a la fuente.
