# Checklist de requisitos del orden: Ordenar la lista de sitios por precio

**Propósito**: Evaluar si los requisitos del orden están completos, claros, consistentes con la spec 001 y cubren
los casos límite, antes de implementar.
**Creado**: 2026-11-25
**Funcionalidad**: [spec.md](../spec.md) · [plan.md](../plan.md) · [contracts/openapi-cambios.yaml](../contracts/openapi-cambios.yaml)

**Nota**: checklist generado por `/speckit-checklist` a partir de la spec y el plan.
**Responsable de la revisión**: quien revisa marca `[x]` solo cuando confirma que el criterio de calidad del
requisito se cumple.
**Significado de la marca**: `[x]` significa que el requisito está bien escrito, no que el código esté listo.

## Completitud de los requisitos

- [ ] CHK001 ¿Están definidas exactamente las opciones del selector y su texto visible? [Completitud, Spec Historia 2]
- [ ] CHK002 ¿Se define cuál es el orden predeterminado cuando el turista no elige ninguno? [Completitud, Spec RF-004]
- [ ] CHK003 ¿Se define qué precio se usa para ordenar un sitio con varios precios? [Completitud, Spec §Casos límite]

## Claridad de los requisitos

- [ ] CHK004 ¿Está claro que «sin precio» significa precio desconocido y no gratis? [Claridad, Spec RF-002]
- [ ] CHK005 ¿Se especifica la regla de desempate cuando dos sitios tienen el mismo precio? [Claridad, Spec RF-003]
- [ ] CHK006 ¿Está definido el texto del error para un valor de orden inválido? [Claridad, Spec CA-8, research D2]

## Consistencia con la spec 001

- [ ] CHK007 ¿El «precio de referencia» usado para ordenar es el mismo que define la spec 001 para la lista? [Consistencia, Spec §Supuestos, spec 001 CA-1]
- [ ] CHK008 ¿El orden por nombre de esta spec usa la misma regla (sin tildes ni mayúsculas) que la spec 001? [Consistencia, Spec CA-5, spec 001 research D5]
- [ ] CHK009 ¿El comportamiento de «Limpiar filtros» es consistente entre ambas specs ahora que incluye el orden? [Consistencia, Spec CA-9, spec 001 CA-14]
- [ ] CHK010 ¿El formato del error 422 de `orden` coincide con el de los demás filtros? [Consistencia, contracts/openapi-cambios.yaml]

## Calidad de los criterios de aceptación

- [ ] CHK011 ¿Cada criterio CA-1 a CA-9 indica un orden o un resultado exacto que se puede comprobar? [Medibilidad, Spec §Escenarios]
- [ ] CHK012 ¿El criterio de éxito CE-001 («una sola acción») se puede medir de forma objetiva? [Medibilidad, Spec CE-001]

## Cobertura de casos límite

- [ ] CHK013 ¿Se define el resultado cuando todos los sitios filtrados carecen de precio? [Caso límite, Spec §Casos límite]
- [ ] CHK014 ¿Se define el resultado del orden cuando los filtros no devuelven sitios? [Caso límite, Spec §Casos límite]
- [ ] CHK015 ¿Se define qué pasa si la dirección compartida trae un orden inválido? [Caso límite, Gap, Spec CA-7 y CA-8]

## Requisitos no funcionales

- [ ] CHK016 ¿Están definidos los requisitos de accesibilidad del selector (etiqueta y uso con teclado)? [Cobertura, Spec RF-008]

## Notas

- Marca `[x]` solo después de confirmar en la revisión que el criterio de calidad del requisito se cumple.
- `/speckit-implement` lee el estado de este checklist como compuerta y no modifica las marcas.
