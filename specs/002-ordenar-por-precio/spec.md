# Especificación: Ordenar la lista de sitios por precio

**Rama**: `feat/002-ordenar-por-precio`

**Creada**: 2026-11-25

**Estado**: Borrador

**Entrada**: pedido en [prompt.md](prompt.md): que el turista pueda ordenar la lista de sitios por precio, de
menor a mayor, además del orden por nombre, con los sitios sin precio conocido al final.

## Clarifications

### Session 2026-11-25

- Q: ¿El selector debe ofrecer también ordenar por precio de mayor a menor, o basta con de menor a mayor? → A: Solo
  de menor a mayor, más el orden por nombre.

## Escenarios de usuario y pruebas *(obligatorio)*

### Historia 1 - Ver primero los sitios más económicos (Prioridad: P1)

Un turista con presupuesto limitado abre la lista de sitios, elige «Ordenar por: Precio (de menor a mayor)» y ve
primero los sitios más económicos. Los sitios de los que no se conoce el precio aparecen al final, para que no se
confundan con sitios gratuitos.

**Por qué esta prioridad**: es todo el valor de la funcionalidad.

**Prueba independiente**: con un catálogo de sitios con distintos precios y algunos sin precio, pedir la lista
ordenada por precio y comprobar el orden exacto.

**Escenarios de aceptación**:

1. **CA-1. Dado** sitios con precios de referencia $20.000, $10.000 y $15.000, **cuando** el turista elige ordenar
   por precio, **entonces** la lista los muestra en el orden $10.000, $15.000, $20.000.
2. **CA-2. Dado** sitios con precio conocido y sitios sin precio conocido, **cuando** se ordena por precio,
   **entonces** todos los sitios con precio aparecen antes que los que no tienen, y los sin precio quedan
   ordenados por nombre.
3. **CA-3. Dado** un sitio gratuito (precio de referencia 0), **cuando** se ordena por precio, **entonces** aparece
   antes que los sitios con precio mayor que 0 y antes que los sitios sin precio.
4. **CA-4. Dado** dos sitios con el mismo precio de referencia, **cuando** se ordena por precio, **entonces** entre
   ellos se ordenan por nombre.

---

### Historia 2 - Elegir el orden y combinarlo con los filtros (Prioridad: P1)

El turista ve un selector «Ordenar por» con las opciones «Nombre (A–Z)» y «Precio (de menor a mayor)». El orden
se mantiene al aplicar los filtros de municipio, categoría y búsqueda.

**Por qué esta prioridad**: sin el selector el turista no puede usar la funcionalidad.

**Prueba independiente**: cambiar el selector y aplicar filtros, y comprobar que la lista respeta ambos.

**Escenarios de aceptación**:

1. **CA-5. Dado** que el turista abre la lista sin elegir orden, **cuando** se muestra, **entonces** está ordenada
   por nombre (como antes de esta funcionalidad) y el selector muestra «Nombre (A–Z)».
2. **CA-6. Dado** que el turista elige «Precio (de menor a mayor)» y además filtra por un municipio, **cuando** se
   actualiza la lista, **entonces** solo aparecen sitios de ese municipio y en orden de precio.
3. **CA-7. Dado** que el turista eligió ordenar por precio, **cuando** comparte o recarga la dirección de la
   lista, **entonces** la lista sigue ordenada por precio.
4. **CA-8. Dado** un valor de orden que no existe, **cuando** se pide la lista con ese orden, **entonces** el
   sistema responde con un mensaje de error claro en español.
5. **CA-9. Dado** que el turista pulsa «Limpiar filtros», **cuando** se limpia, **entonces** el orden también
   vuelve a «Nombre (A–Z)».

---

### Casos límite

- Catálogo vacío o filtros sin resultados: el orden no cambia los mensajes existentes de la spec 001.
- Todos los sitios sin precio: con orden por precio la lista queda igual que con orden por nombre.
- Un sitio con varios precios se ordena por su precio de referencia (el menor conocido), el mismo que ya muestra
  la lista.

## Requisitos *(obligatorio)*

### Requisitos funcionales

- **RF-001**: El sistema MUST permitir ordenar la lista por nombre (A–Z) o por precio de referencia de menor a
  mayor (CA-1, CA-5).
- **RF-002**: Con orden por precio, los sitios sin precio conocido MUST ir después de todos los que tienen precio,
  ordenados por nombre entre sí; nunca se tratan como gratuitos (CA-2, CA-3).
- **RF-003**: Los empates de precio MUST resolverse por nombre (CA-4).
- **RF-004**: El orden predeterminado MUST ser por nombre (CA-5).
- **RF-005**: El orden MUST combinarse con los filtros existentes de municipio, categoría y búsqueda (CA-6).
- **RF-006**: El orden elegido MUST conservarse en la dirección de la lista para poder compartirla o recargarla
  (CA-7), y «Limpiar filtros» lo devuelve al predeterminado (CA-9).
- **RF-007**: Un valor de orden inválido MUST rechazarse con un mensaje de error en español (CA-8).
- **RF-008**: El selector MUST tener una etiqueta visible y usarse con teclado.

### Entidades clave

- **Orden de la lista**: criterio con dos valores posibles: por nombre (predeterminado) o por precio. No se guarda;
  vive en la dirección de la lista.

## Criterios de éxito *(obligatorio)*

### Resultados medibles

- **CE-001**: Un turista ve el sitio más económico del catálogo en el primer lugar de la lista con una sola acción
  (elegir el orden por precio).
- **CE-002**: El 100 % de los sitios sin precio conocido aparece después de todos los sitios con precio cuando se
  ordena por precio.
- **CE-003**: El 100 % de los criterios CA-1 a CA-9 tiene al menos una prueba automatizada que pasa.

## Supuestos

- Solo se ofrece el orden de menor a mayor; de mayor a menor queda fuera de alcance (aclaración del 2026-11-25).
- El precio de referencia es el que ya calcula la spec 001 (el menor precio conocido del sitio).
- No se ordena por otros criterios (municipio, categoría, distancia).
