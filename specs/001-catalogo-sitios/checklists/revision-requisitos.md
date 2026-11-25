# Checklist de revisión de requisitos: Catálogo de sitios turísticos del Huila

**Propósito**: Evaluar la calidad de los requisitos escritos (completitud, claridad, consistencia,
medibilidad y cobertura) sobre datos turísticos, API y experiencia de usuario, antes de fusionar la spec 001.
**Creado**: 2026-11-25
**Funcionalidad**: [spec.md](../spec.md) · [plan.md](../plan.md) · [data-model.md](../data-model.md) ·
[contracts/openapi.yaml](../contracts/openapi.yaml)

**Nota**: checklist generado por `/speckit-checklist` a partir de la spec, el plan y las tareas.
**Responsable de la revisión**: la persona que revisa marca `[x]` solo cuando confirma que el criterio de calidad
del requisito se cumple.
**Significado de la marca**: `[x]` significa que el requisito está bien escrito; no significa que la implementación
esté terminada.

## Completitud de los requisitos

- [ ] CHK001 ¿Están definidos los campos obligatorios y opcionales de una ficha de sitio en un solo lugar canónico? [Completitud, data-model §Reglas de rechazo]
- [ ] CHK002 ¿Se define qué se muestra cuando un sitio tiene precios conocidos y desconocidos a la vez? [Completitud, Spec §Casos límite]
- [ ] CHK003 ¿Están especificados los estados de carga, vacío, sin resultados, no encontrado y error para ambas pantallas? [Completitud, Spec RF-007]
- [ ] CHK004 ¿Se define el comportamiento cuando falla la carga de las listas de filtros (municipios y categorías)? [Completitud, Gap → research D11 ajuste R8]
- [ ] CHK005 ¿Se especifica el formato del cuerpo de error para todos los códigos que expone la API (404, 422, 405, 500)? [Completitud, contracts/openapi.yaml]

## Claridad de los requisitos

- [ ] CHK006 ¿Está definido exactamente el formato del precio, incluido el separador de miles y la abreviatura de cada mes? [Claridad, Spec RF-003, research D8]
- [ ] CHK007 ¿Se define sin ambigüedad qué es el «precio de referencia» de la lista y cuándo se antepone «Desde»? [Claridad, Spec CA-1, Aclaración 3]
- [ ] CHK008 ¿Está definida la regla para formar el identificador legible (slug), incluidas tildes, ñ y signos? [Claridad, Spec CA-20, research D6]
- [ ] CHK009 ¿Se define qué significa «sin distinguir mayúsculas, minúsculas ni tildes» en la búsqueda, incluidos los comodines `%` y `_`? [Claridad, Spec CA-12, research D5]
- [ ] CHK010 ¿Está explícito si los bordes de las coordenadas del Huila son inclusivos o exclusivos? [Claridad, Spec CA-17, research D9]
- [ ] CHK011 ¿Se define qué fecha representa `fecha_referencia_precio`: la de consulta o la de publicación del dato? [Ambigüedad, Constitución II, revision.md D-1]

## Consistencia de los requisitos

- [ ] CHK012 ¿Coinciden las 7 categorías entre la spec, el modelo de datos, el contrato y la skill `datos-turisticos`? [Consistencia, Spec Aclaración 1]
- [ ] CHK013 ¿Coinciden los límites de longitud (nombre 120, concepto 80, descripción 400, horario 200, cómo llegar 500, URL 500) entre la spec, el modelo de datos y el contrato? [Consistencia, data-model §Reglas 1, 7 y 8]
- [ ] CHK014 ¿Son consistentes los textos visibles entre la spec y la regla `frontend-angular.md`? [Consistencia, Spec CA-5, CA-9, CA-14]
- [ ] CHK015 ¿Es consistente el tratamiento de «gratis» (0) frente a «desconocido» (null) en la spec, el contrato y la skill? [Consistencia, Spec CA-3, CA-4]

## Calidad de los criterios de aceptación

- [ ] CHK016 ¿Cada criterio CA-1 a CA-20 tiene un resultado esperado exacto y verificable (texto, conteo o código)? [Medibilidad, Spec §Escenarios]
- [ ] CHK017 ¿Los criterios de éxito CE-001, CE-004 y CE-005 indican cómo y en qué condiciones se miden? [Medibilidad, Spec §Criterios de éxito, quickstart 6 a 9]
- [ ] CHK018 ¿Está definido el texto exacto de los mensajes de error 422 que ve el turista, o solo su forma? [Medibilidad, Spec CA-15]

## Cobertura de escenarios y casos límite

- [ ] CHK019 ¿Se cubren los escenarios de recuperación de la carga del catálogo (ficha inválida en una recarga, catálogo anterior intacto)? [Cobertura, Recuperación, data-model §párrafo final]
- [ ] CHK020 ¿Se definen requisitos para entradas con caracteres de control o de longitud excesiva en los filtros? [Cobertura, Caso límite, research D11 ajustes S1 y S2]
- [ ] CHK021 ¿Se especifica qué pasa con dos fichas cuyos nombres distintos producen el mismo slug? [Caso límite, Spec CA-19]
- [ ] CHK022 ¿Se define qué ve el turista cuando una fuente o el enlace de OpenStreetMap no responden? [Caso límite, Spec §Supuestos]

## Requisitos no funcionales

- [ ] CHK023 ¿Están definidos los requisitos de accesibilidad para todos los elementos interactivos (selectores, búsqueda, enlaces que abren otra pestaña)? [Cobertura, Spec RF-011]
- [ ] CHK024 ¿El requisito de contraste suficiente está cuantificado (por ejemplo, nivel AA)? [Claridad, Spec RF-011, quickstart escenario 7]
- [ ] CHK025 ¿Se documenta que la API es pública, de solo lectura, y qué superficie expone (incluida la documentación automática)? [Supuesto, Spec RF-012, revision.md S6]

## Dependencias y supuestos

- [ ] CHK026 ¿Está documentada la fuente de la lista de 37 municipios y su validación frente a una fuente oficial? [Dependencia, revision.md D-2, backend/datos/municipios.json]
- [ ] CHK027 ¿Está documentado el supuesto de disponibilidad de OpenStreetMap y su impacto en la ficha? [Supuesto, Spec §Supuestos]

## Notas

- Marca `[x]` solo después de confirmar en la revisión que el criterio de calidad del requisito se cumple.
- Deja sin marcar lo que todavía necesite aclaración, corrección o evaluación de quien revisa.
- `/speckit-implement` lee el estado de este checklist como compuerta y no modifica las marcas.
- `checklists/requirements.md` tiene su propio ciclo, que mantienen `/speckit-specify` y `/speckit-clarify`.
