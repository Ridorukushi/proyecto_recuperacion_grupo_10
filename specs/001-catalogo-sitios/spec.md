# Especificación: Catálogo de sitios turísticos del Huila

**Rama**: `feat/001-catalogo-sitios`

**Creada**: 2026-11-24

**Estado**: Aprobada por el grupo (2026-11-24)

**Entrada**: pedido del grupo en [prompt.md](prompt.md): catálogo web de sitios turísticos del Huila con
lista filtrable y buscable, y ficha de cada sitio con precio aproximado en COP, horario, cómo llegar,
fuente y enlace al mapa.

## Clarifications

### Session 2026-11-24

- Q: ¿Qué lista de categorías debe aceptar el catálogo? → A: Las 7 de la skill `datos-turisticos`:
  arqueología, naturaleza, aventura, cultura, religioso, gastronomía y termales.
- Q: ¿Cómo debe verse la dirección web de la ficha de un sitio cuando el turista la copia o la comparte?
  → A: Con un identificador legible derivado del nombre, en minúsculas, sin tildes y con guiones
  (`/sitios/desierto-de-la-tatacoa`); el nombre de cada sitio es único.
- Q: Si un sitio tiene varios precios, ¿cuál se muestra en la lista? → A: El menor de los precios conocidos,
  como «desde»: `Desde $15.000 COP (aprox., consultado en nov. 2026)`; con un solo precio no se antepone «Desde».
  Si el menor es 0, se muestra «Gratis (hay otras tarifas)» (ajuste tras `/speckit-analyze`, hallazgo I1).

## Escenarios de usuario y pruebas *(obligatorio)*

### Historia 1 - Ver la lista de sitios (Prioridad: P1)

Un turista entra al catálogo y ve todos los sitios turísticos disponibles del Huila, cada uno con su nombre,
municipio, categoría y precio aproximado, para hacerse una idea rápida de qué visitar.

**Por qué esta prioridad**: sin la lista no hay catálogo; es la base de todo lo demás y ya le sirve al turista
por sí sola.

**Prueba independiente**: con el catálogo inicial cargado, abrir la lista y comprobar que aparecen todos los
sitios con esos cuatro datos.

**Escenarios de aceptación**:

1. **CA-1. Dado** un catálogo con sitios, **cuando** el turista abre la lista, **entonces** ve todos los sitios
   ordenados alfabéticamente por nombre, cada uno con nombre, municipio, categoría y precio de referencia
   (el menor de sus precios conocidos, con «Desde» si tiene más de uno).
2. **CA-2. Dado** un sitio con precio conocido de $25.000, consultado en noviembre de 2026, **cuando** aparece en la lista
   o en su ficha, **entonces** el precio se muestra exactamente como `$25.000 COP (aprox., consultado en nov. 2026)`.
3. **CA-3. Dado** un sitio sin precio conocido, **cuando** aparece en la lista o en su ficha, **entonces** se
   muestra «Precio no disponible» y nunca «$0».
4. **CA-4. Dado** un sitio cuya entrada es gratuita (precio conocido igual a 0), **cuando** se muestra,
   **entonces** aparece «Gratis», distinto de «Precio no disponible». Si además tiene otros precios mayores,
   en la lista aparece «Gratis (hay otras tarifas)».
5. **CA-5. Dado** que el catálogo todavía se está cargando, no tiene sitios o no se pudo obtener, **cuando** el
   turista abre la lista, **entonces** ve respectivamente un aviso de carga, el mensaje «No hay sitios para
   mostrar» o un mensaje de error en español con la opción de reintentar.

---

### Historia 2 - Ver la ficha de un sitio (Prioridad: P1)

El turista elige un sitio de la lista y ve su ficha completa: descripción, precios, horario, cómo llegar, la
fuente de la información y un enlace para ver su ubicación en un mapa.

**Por qué esta prioridad**: es donde el turista obtiene la información para decidir y desplazarse; junto con la
lista forma el producto mínimo.

**Prueba independiente**: abrir la ficha de un sitio conocido y comprobar cada campo contra los datos cargados.

**Escenarios de aceptación**:

1. **CA-6. Dado** un sitio del catálogo, **cuando** el turista abre su ficha, **entonces** ve nombre, municipio,
   categoría, descripción, cada precio con su concepto (por ejemplo «Entrada adulto»), horario, cómo llegar
   y la lista de fuentes como enlaces.
2. **CA-7. Dado** un sitio con coordenadas, **cuando** el turista pulsa «Ver en mapa», **entonces** se abre
   OpenStreetMap en una pestaña nueva centrado en esas coordenadas.
3. **CA-8. Dado** un sitio con horario o cómo llegar desconocidos, **cuando** se muestra la ficha, **entonces**
   ese campo indica «No disponible» en lugar de quedar en blanco o mostrar un dato supuesto.
4. **CA-9. Dado** un identificador de sitio que no existe (por ejemplo `/sitios/sitio-que-no-existe`),
   **cuando** el turista intenta abrir esa ficha, **entonces** ve el mensaje «Sitio no encontrado» y un enlace
   para volver a la lista.
5. **CA-20. Dado** el sitio «Desierto de la Tatacoa», **cuando** el turista abre su ficha, **entonces** la
   dirección web termina en `/sitios/desierto-de-la-tatacoa` y al abrir esa dirección directamente se ve la
   misma ficha.

---

### Historia 3 - Filtrar y buscar sitios (Prioridad: P2)

El turista reduce la lista eligiendo un municipio, una categoría o escribiendo parte del nombre del sitio, para
encontrar rápido lo que le interesa.

**Por qué esta prioridad**: con 10 a 15 sitios la lista ya es usable sin filtros; los filtros mejoran la
experiencia pero no son imprescindibles para el primer valor.

**Prueba independiente**: aplicar cada filtro por separado y combinado, y comprobar que solo quedan los sitios
que cumplen.

**Escenarios de aceptación**:

1. **CA-10. Dado** el catálogo, **cuando** el turista elige un municipio, **entonces** la lista muestra solo los
   sitios de ese municipio.
2. **CA-11. Dado** el catálogo, **cuando** el turista elige una categoría, **entonces** la lista muestra solo los
   sitios de esa categoría.
3. **CA-12. Dado** el catálogo, **cuando** el turista escribe parte de un nombre (por ejemplo «tatacoa» o
   «TATACOA»), **entonces** la lista muestra los sitios cuyo nombre lo contiene, sin distinguir mayúsculas,
   minúsculas ni tildes.
4. **CA-13. Dado** que el turista combina municipio, categoría y texto, **cuando** aplica los filtros,
   **entonces** solo aparecen los sitios que cumplen todos a la vez.
5. **CA-14. Dado** una combinación de filtros sin resultados, **cuando** se aplica, **entonces** se muestra «No
   hay sitios que coincidan con tu búsqueda» y la opción de limpiar los filtros.
6. **CA-15. Dado** un municipio o una categoría que no existen en el catálogo, **cuando** se piden, **entonces**
   el sistema responde con un mensaje de error claro en español y no con una lista vacía silenciosa.

---

### Historia 4 - Catálogo inicial con datos verificables (Prioridad: P1)

El grupo carga el catálogo inicial con sitios reales del Huila. Cada dato viene de una fuente consultada, y lo
que no se conoce se deja vacío.

**Por qué esta prioridad**: sin datos reales el catálogo no tiene valor, y un dato inventado es un defecto grave
según la constitución (principio II).

**Prueba independiente**: validar todas las fichas del catálogo inicial contra las reglas de datos y comprobar
que las inválidas se rechazan.

**Escenarios de aceptación**:

1. **CA-16. Dado** el catálogo inicial, **cuando** se carga, **entonces** contiene entre 10 y 15 sitios, todos
   con nombre, municipio, categoría, coordenadas y al menos una fuente.
2. **CA-17. Dado** una ficha con coordenadas fuera del Huila (latitud fuera de 1.5–3.9 o longitud fuera de
   −76.6–−74.4), **cuando** se intenta cargar, **entonces** se rechaza con un mensaje que indica el campo
   inválido.
3. **CA-18. Dado** una ficha sin fuente, sin nombre, con un municipio que no es del Huila o con una categoría
   fuera de la lista permitida, **cuando** se intenta cargar, **entonces** se rechaza indicando el campo
   inválido.
4. **CA-19. Dado** una ficha con algún precio, **cuando** se carga sin fecha de consulta del precio, **entonces**
   se rechaza; y un precio negativo también se rechaza. Dos fichas con el mismo nombre también se rechazan.

---

### Casos límite

- Nombre de búsqueda vacío o solo con espacios: se trata como «sin búsqueda» y se muestran todos los sitios.
- Texto de búsqueda muy largo (más de 100 caracteres): se rechaza con un mensaje claro.
- Sitio con varios precios (adulto, niño, extranjero): en la lista se muestra el menor antecedido de «Desde»;
  en la ficha se muestran todos con su concepto. Si el menor es gratis (0), la lista muestra «Gratis (hay otras
  tarifas)» en lugar de «Desde Gratis».
- Nombre de sitio de más de 120 caracteres o concepto de precio de más de 80: la ficha se rechaza al cargar.
- Sitio con unos precios conocidos y otros no: solo se muestran los conocidos; si ninguno lo es, «Precio no
  disponible».
- Fuente que ya no responde: el enlace se muestra igual; verificar fuentes caídas queda fuera de esta spec.
- Pantalla de celular angosta (360 px): la lista y la ficha se leen sin desplazamiento horizontal.

## Requisitos *(obligatorio)*

### Requisitos funcionales

- **RF-001**: El sistema MUST mostrar la lista de todos los sitios del catálogo, ordenada por nombre, con
  nombre, municipio, categoría y precio de referencia: el menor de sus precios conocidos, antecedido de
  «Desde» cuando hay más de uno (CA-1).
- **RF-002**: El sistema MUST mostrar la ficha de un sitio con todos sus datos y sus fuentes como enlaces (CA-6).
  Cada ficha tiene una dirección web estable con un identificador legible derivado del nombre (en minúsculas,
  sin tildes y con guiones), que se puede compartir y abrir directamente (CA-20).
- **RF-003**: El sistema MUST mostrar los precios en COP con el formato `$25.000 COP (aprox., consultado en
  <mes abreviado> <año>)`, «Gratis» cuando el precio conocido es 0 y «Precio no disponible» cuando se
  desconoce (CA-2, CA-3, CA-4).
- **RF-004**: El sistema MUST ofrecer en cada ficha un enlace «Ver en mapa» a OpenStreetMap con las coordenadas
  del sitio, que se abre en una pestaña nueva (CA-7).
- **RF-005**: Los usuarios MUST poder filtrar la lista por municipio, por categoría y por texto del nombre, por
  separado o combinados; la búsqueda no distingue mayúsculas, minúsculas ni tildes (CA-10 a CA-13).
- **RF-006**: El sistema MUST validar en el servidor los filtros recibidos y responder con un error en español
  cuando el municipio o la categoría no son válidos o la búsqueda supera 100 caracteres (CA-15).
- **RF-007**: El sistema MUST mostrar estados de carga, vacío, sin resultados, no encontrado y error, todos en
  español (CA-5, CA-9, CA-14).
- **RF-008**: El sistema MUST rechazar al cargar cualquier ficha que incumpla las reglas de datos: campos
  obligatorios, nombre único, municipio del Huila, categoría permitida, coordenadas dentro del Huila, precio entero ≥ 0 y
  fecha de consulta cuando hay precios (CA-17 a CA-19).
- **RF-009**: El catálogo inicial MUST contener entre 10 y 15 sitios reales del Huila, cada uno con al menos una
  fuente; los datos desconocidos se dejan vacíos y nunca se inventan (CA-16).
- **RF-010**: Un dato desconocido de horario o cómo llegar MUST mostrarse como «No disponible» (CA-8).
- **RF-011**: La interfaz MUST ser usable en celular (desde 360 px de ancho) y cumplir accesibilidad básica:
  navegación con teclado, texto alternativo en imágenes si las hay y contraste suficiente.
- **RF-012**: El catálogo MUST ser de solo lectura para el turista: no hay creación, edición ni borrado de sitios
  desde la web.

### Entidades clave

- **Sitio turístico**: lugar que se puede visitar. Tiene un identificador legible único (derivado del nombre,
  que también es único), nombre, municipio, categoría, descripción breve (máx.
  400 caracteres), latitud, longitud, horario, cómo llegar, fecha de consulta del precio y una o más fuentes.
- **Precio**: valor aproximado en COP de un concepto del sitio (por ejemplo, «Entrada adulto»). Pertenece a un
  sitio; un sitio puede tener cero o varios.
- **Fuente**: enlace de donde salió la información del sitio. Pertenece a un sitio; cada sitio tiene al menos una.
- **Municipio**: uno de los 37 municipios del Huila. Lista fija.
- **Categoría**: tipo de sitio, de una lista fija de 7: arqueología, naturaleza, aventura, cultura, religioso,
  gastronomía y termales.

## Criterios de éxito *(obligatorio)*

### Resultados medibles

- **CE-001**: Un turista encuentra la ficha de un sitio concreto que conoce por nombre en menos de 30 segundos
  desde que abre el catálogo.
- **CE-002**: El 100 % de los sitios del catálogo inicial tiene al menos una fuente y coordenadas dentro del
  Huila; el 0 % tiene datos sin fuente.
- **CE-003**: El 100 % de los criterios de aceptación CA-1 a CA-20 tiene al menos una prueba automatizada que
  pasa.
- **CE-004**: La lista y la ficha se muestran completas en menos de 2 segundos con una conexión móvil normal.
- **CE-005**: En una pantalla de 360 px de ancho, ninguna vista del catálogo necesita desplazamiento horizontal.

## Supuestos

- El turista no necesita cuenta ni iniciar sesión para consultar el catálogo.
- El catálogo inicial lo arma el grupo con el `curador-datos` y se carga desde archivos del repositorio; no hay
  panel de administración en esta spec.
- La lista de 37 municipios del Huila es fija y se carga con el catálogo.
- Las categorías son las 7 de la skill `datos-turisticos` (decidido en la aclaración del 2026-11-24).
- Imágenes de los sitios, mapa embebido, asistente con IA, cuentas de usuario, favoritos y edición desde la web
  quedan fuera de alcance.
- El enlace «Ver en mapa» depende de que OpenStreetMap esté disponible; si no lo está, el resto de la ficha
  funciona igual.
