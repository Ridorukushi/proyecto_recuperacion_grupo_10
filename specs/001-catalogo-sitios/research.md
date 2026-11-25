# Investigación (Fase 0): 001-catalogo-sitios

Cada decisión resuelve una incógnita del contexto técnico o un hueco del informe del `explorador`
(numerados como en ese informe: H1…H22).

## D1. Base de datos en pruebas y en el CI (H16)
- **Decisión:** PostgreSQL 16 real. En el CI se usa un servicio `postgres:16` en el job `backend`; en local,
  PostgreSQL instalado en el computador de cada integrante. La URL de la base de pruebas llega por la variable
  `DATABASE_URL_PRUEBAS`.
- **Razón:** decisión del grupo; la búsqueda sin tildes y el orden se prueban sobre la misma base que se usa
  en producción.
- **Alternativas:** SQLite en memoria (descartada por el grupo: se comporta distinto); Docker Compose
  (descartado: exige Docker en cada computador).

## D2. Quién prepara el esqueleto (H17)
- **Decisión:** el orquestador, con permiso del grupo en cada comando, en una fase **Preparación** previa al
  Red: crea `backend/.venv` con `uv venv`, instala `requirements.txt` con `uv pip install`, crea el proyecto
  Angular con `ng new`, ejecuta `npm install` y agrega el servicio PostgreSQL al CI.
- **Razón:** decisión del grupo; no se amplían los permisos de los subagentes.
- **Límite:** el orquestador solo deja archivos de configuración y lo que genera `ng new`; no escribe
  lógica de la aplicación ni pruebas.

## D3. Cómo ejecutan pytest los agentes en Windows (H19, H20)
- **Decisión:** `cd backend && uv run pytest -q`. `uv run` encuentra solo el entorno `backend/.venv`, así
  que no hace falta activarlo. `backend/pytest.ini` fija `pythonpath = .` y `testpaths = tests` para que
  `pytest`, `python -m pytest` (CI) y `uv run pytest` importen `app` igual.
- **Alternativas:** activar el venv (el hook no lo permite); rutas `.venv\Scripts\python` (no permitidas).

## D4. Acceso a datos
- **Decisión:** SQLAlchemy 2 (estilo ORM con `select()`) con el driver `psycopg` 3. El esquema se versiona
  en `backend/db/001_esquema.sql` y se aplica con la función `crear_esquema()`; las pruebas lo aplican en
  una base limpia por sesión.
- **Razón:** consultas parametrizadas por defecto (regla `backend-api.md`). Un solo archivo SQL basta para
  esta spec; una herramienta de migraciones (Alembic) sería YAGNI hoy.

## D5. Búsqueda sin tildes y orden alfabético (H2, H21)
- **Decisión:** una función `normalizar(texto)`: NFD, quita las marcas diacríticas, minúsculas y espacios
  colapsados. Con NFD la «ñ» pasa a «n» («Ñame» → «name»); se acepta. Cada sitio guarda
  `nombre_normalizado`; la búsqueda compara `normalizar(q)` con `LIKE '%…%'`, escapando `%`, `_` y `\`.
  El orden es por `nombre_normalizado`.
- **Razón:** no depende de la extensión `unaccent` ni de la colación del sistema operativo, que cambia entre
  Windows y Ubuntu.

## D6. Identificador legible (slug) (H1)
- **Decisión:** `slug = normalizar(nombre)`; todo lo que no sea `a-z0-9` se convierte en `-`, los guiones se
  colapsan y se quitan los de los extremos. Ejemplo: «Desierto de la Tatacoa» → `desierto-de-la-tatacoa`.
  `slug` y `nombre` son únicos en la base; dos fichas que producen el mismo slug se rechazan al cargar.
  Un slug que no cumple `^[a-z0-9-]{1,120}$` responde 404, igual que uno inexistente.

## D7. Claves y etiquetas de municipios y categorías (H3, H14)
- **Decisión:** se guarda una **clave** sin tildes (`garzon`, `arqueologia`) y se muestra una **etiqueta**
  (`Garzón`, `Arqueología`). Los filtros de la API reciben claves. Los 37 municipios viven en
  `backend/datos/municipios.json` con su fuente; el `curador-datos` los arma. Las 7 categorías son una lista
  fija en el código.
- Endpoint nuevo `GET /api/filtros` entrega ambas listas para los selectores (H10).

## D8. Formato del precio (H4, H5, H6)
- **Decisión:** el backend entrega números (`valor_cop`, `fecha_referencia_precio`) y el frontend formatea en
  una función pura `formatearPrecio`. Reglas:
  - conocido > 0: `$25.000 COP (aprox., consultado en nov. 2026)`. El separador de miles es el punto y se
    pone en código, sin depender de `Intl`;
  - conocido = 0: `Gratis`, sin sufijo de fecha;
  - desconocido: `Precio no disponible`;
  - en la lista, con más de un precio conocido: `Desde ` + el formato del menor. Si el menor es 0:
    `Gratis (hay otras tarifas)`.
  - Meses: `ene., feb., mar., abr., may., jun., jul., ago., sept., oct., nov., dic.`
- El campo `aproximado` de la skill se elimina: todos los precios son aproximados por constitución.
- Un concepto con `valor_cop` ausente se descarta al cargar (la spec dice «solo se muestran los conocidos»).
  `fecha_referencia_precio` es obligatoria si queda al menos un precio conocido.

## D9. Campos obligatorios y bordes (H7, H12)
- **Obligatorios:** `nombre`, `municipio`, `categoria`, `latitud`, `longitud` y `fuentes` (≥ 1 URL http/https).
- **Opcionales:** `descripcion` (≤ 400 caracteres), `horario`, `como_llegar`, `precios`.
- Bordes del Huila **inclusivos**: latitud 1.5 ≤ x ≤ 3.9 y longitud −76.6 ≤ x ≤ −74.4.

## D10. Carga del catálogo (H11)
- **Decisión:** función `cargar_catalogo(sesion, ruta_sitios, ruta_municipios)` en `backend/app/carga.py`.
  Valida todas las fichas con Pydantic y, si alguna falla, no guarda ninguna (todo o nada). Lanza
  `ErrorCarga` con mensajes `«<nombre o índice>: <campo>: <motivo>»`. Se ejecuta a mano con
  `uv run python -m app.carga` (grupo u orquestador); las pruebas llaman la función con JSON temporales.

## D11. Errores en español (H9)
- **Decisión:** manejadores propios para `RequestValidationError` (422) y `HTTPException` (404). Cuerpo:
  `{"detalle": "<mensaje en español>"}`, sin `loc`, trazas ni SQL.
  Ejemplos: `El municipio «xyz» no existe en el Huila.`, `Sitio no encontrado.`
- Ajustes tras la revisión:
  - **S1 y S2:** `municipio` y `categoria` aceptan como máximo 60 caracteres con el patrón `^[a-z0-9-]+$`; `q`
    no acepta caracteres de control. Todo lo demás responde 422, y el mensaje nunca repite un valor de más de
    60 caracteres.
  - **S7:** cualquier error inesperado responde 500 con `{"detalle": "Error interno. Intenta más tarde."}`.
  - **R4:** en el frontend, un 422 muestra el `detalle` del servidor junto con «Limpiar filtros».

## D12. Frontend (H18, H22, H8)
- **Decisión:** Angular 21 creado con `ng new`; desde la versión 21 `ng test` usa vitest, así que el
  comando del CI `npx ng test --watch=false` sirve sin cambios.
- La URL de la API es relativa (`/api`) y en desarrollo pasa por `proxy.conf.json` hacia `http://localhost:8000`;
  así no hace falta CORS en desarrollo. CORS queda en el backend, controlado por `ORIGENES_PERMITIDOS`.
- OpenStreetMap: `https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}`, con
  `target="_blank"` y `rel="noopener noreferrer"`.
- Los textos de vacío son los de la spec; la regla `frontend-angular.md` se ajusta para que no los contradiga.

## D13. Dependencias
- Backend (`backend/requirements.txt`): `fastapi`, `uvicorn[standard]`, `sqlalchemy>=2`, `psycopg[binary]>=3`,
  `pydantic-settings`, `pytest`, `httpx`, `ruff`. Las versiones exactas se fijan al instalar.
- Frontend: lo que trae `ng new`; ninguna librería extra (sin librería de mapas).

## D14. Datos reales (H13)
- La ficha de Tatacoa de la skill es ilustrativa. El `curador-datos` arma `sitios.json` desde cero con
  fuentes y fechas consultadas. CA-20 exige que el catálogo incluya el Desierto de la Tatacoa.
