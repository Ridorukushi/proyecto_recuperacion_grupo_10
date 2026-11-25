---
name: datos-turisticos
description: Formato y reglas de validación de una ficha de sitio turístico del Huila (precios COP aproximados, coordenadas, fuentes). Úsala al crear, importar, validar o mostrar datos del catálogo.
---

# Ficha de sitio turístico del Huila

Formato de referencia de un sitio (JSON). El modelo definitivo de base de datos se fija en
`/speckit-plan`; si cambia, se actualiza esta skill.

```json
{
  "nombre": "Desierto de la Tatacoa",
  "municipio": "Villavieja",
  "categoria": "naturaleza",
  "descripcion": "Texto propio y breve (máx. 400 caracteres).",
  "latitud": 3.2333,
  "longitud": -75.1667,
  "precios": [
    { "concepto": "Entrada observatorio adulto", "valor_cop": 0, "aproximado": true }
  ],
  "fecha_referencia_precio": "2026-11-24",
  "horario": "",
  "como_llegar": "",
  "fuentes": ["https://..."]
}
```

Los valores del ejemplo son ilustrativos; no usarlos como datos reales sin verificar.

## Reglas de validación
- `nombre`, `municipio`, `categoria`, `latitud`, `longitud` y al menos una `fuente`: obligatorios.
- `municipio`: uno de los 37 municipios del Huila.
- `categoria`: `naturaleza`, `arqueologia`, `cultura`, `aventura`, `gastronomia`, `religioso`,
  `termales`.
- Coordenadas: latitud 1.5 a 3.9 y longitud −76.6 a −74.4.
- `valor_cop`: entero ≥ 0; `0` significa gratis, campo ausente significa desconocido.
- Si hay precios, `fecha_referencia_precio` es obligatoria (formato AAAA-MM-DD).
- Campos desconocidos van vacíos: nunca se rellenan con suposiciones.

## Cómo se muestra al usuario
- Precio: `$25.000 COP (aprox., consultado en nov. 2026)`.
- Sin precio: "Precio no disponible", nunca "$0".
- Siempre mostrar el enlace a la fuente.
