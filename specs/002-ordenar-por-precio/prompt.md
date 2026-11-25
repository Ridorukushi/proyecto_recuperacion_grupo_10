# 002-ordenar-por-precio: prompt

Pedido con el que se arrancó la spec (2026-11-25), con la fórmula del curso:

- **Qué quiero:** que el turista pueda ordenar la lista de sitios por precio, de menor a mayor, además del orden
  por nombre que ya existe. Un selector «Ordenar por» con dos opciones: «Nombre (A–Z)» (predeterminado) y
  «Precio (de menor a mayor)». Los sitios sin precio conocido van al final, ordenados por nombre.
- **Para quién:** turistas con presupuesto limitado que quieren ver primero los sitios más económicos.
- **Contexto:** la spec 001 ya entrega la lista con filtros por municipio, categoría y nombre, y cada sitio tiene un
  precio de referencia (el menor de sus precios conocidos) o ninguno.
- **Formato:** spec con criterios de aceptación numerados (CA-n) que se puedan probar; cambio en la API de la lista y
  en la pantalla de lista.
- **Restricciones:** pruebas primero; todo en español; los sitios sin precio nunca se tratan como gratis; el orden
  debe funcionar junto con los filtros existentes; sin dependencias nuevas.

**Skills que debe usar:** las `speckit-*` en su flujo completo (specify, clarify, plan, checklist, tasks, analyze,
implement, converge).

**Aprobaciones:** pendiente.
