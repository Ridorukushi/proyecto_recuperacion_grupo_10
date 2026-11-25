# Guía rápida de validación: 002-ordenar-por-precio

Requisitos y preparación: los mismos de [la spec 001](../001-catalogo-sitios/quickstart.md).

## Pruebas
```powershell
cd backend ; uv run pytest -q
cd frontend ; npx ng test --watch=false
```

## Escenarios manuales (con el catálogo real cargado)
1. `http://localhost:8000/api/sitios?orden=precio`: primero el Desierto de la Tatacoa ($10.000), luego Termales de
   Rivera ($15.000) y el Parque Arqueológico de San Agustín ($20.000); después los 7 sitios sin precio, por nombre
   (CA-1, CA-2).
2. `http://localhost:8000/api/sitios?orden=xyz`: 422 con mensaje en español (CA-8).
3. En `http://localhost:4200/sitios`, elegir «Ordenar por: Precio (de menor a mayor)»: la URL incluye `orden=precio`
   y al recargar se conserva (CA-7).
4. Elegir además un municipio: solo sus sitios, en orden de precio (CA-6). «Limpiar filtros» vuelve a «Nombre (A–Z)»
   (CA-9).
