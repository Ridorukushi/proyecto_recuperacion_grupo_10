# Guía rápida de validación: 001-catalogo-sitios

Cómo comprobar de punta a punta que la spec funciona. El contrato está en
[contracts/openapi.yaml](contracts/openapi.yaml) y el modelo en [data-model.md](data-model.md).

## Requisitos previos
- Python 3.12 y `uv`; Node 22 y npm; PostgreSQL 16 instalado en el computador.
- Dos bases vacías: `turismo` (para usar la app) y `turismo_pruebas` (para las pruebas).
- `backend/.env`, copiado de `backend/.env.example` y llenado por cada persona. Ningún agente lo lee.

## Preparar (una vez)
```powershell
cd backend
uv venv
uv pip install -r requirements.txt
cd ..\frontend
npm install
```

## Pruebas (lo mismo que corre el CI)
```powershell
cd backend ; uv run pytest -q          # en el CI: python -m pytest -q
cd frontend ; npx ng test --watch=false
cd frontend ; npm run build
node --test .claude/hooks/hooks.test.mjs
```
Esperado: todo en verde. Cada criterio CA-n tiene al menos una prueba (ver la tabla del plan).

## Cargar el catálogo y abrir la app
```powershell
cd backend ; uv run python -m app.carga             # crea el esquema y carga backend/datos/*.json
cd backend ; uv run uvicorn app.main:app --reload   # API en http://localhost:8000
cd frontend ; npx ng serve                          # app en http://localhost:4200 (proxy /api)
```

## Escenarios manuales
1. `http://localhost:4200/sitios`: se ven entre 10 y 15 sitios, ordenados por nombre (CA-1, CA-16).
2. Escribir «TATACOA» en la búsqueda: queda el Desierto de la Tatacoa (CA-12).
3. Abrir su ficha: la dirección es `/sitios/desierto-de-la-tatacoa` (CA-20); «Ver en mapa» abre
   OpenStreetMap en otra pestaña (CA-7).
4. `http://localhost:4200/sitios/no-existe`: aparece «Sitio no encontrado» (CA-9).
5. `http://localhost:8000/api/sitios?municipio=xyz`: responde 422 con un mensaje en español (CA-15).
6. Herramientas del navegador a 360 px de ancho: sin desplazamiento horizontal en la lista y la ficha (CE-005).
7. Navegar la lista y la ficha solo con Tab y Enter (RF-011).
