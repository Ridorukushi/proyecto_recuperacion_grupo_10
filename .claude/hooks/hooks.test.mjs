// Pruebas de los hooks del arnés. Ejecutar con: node --test .claude/hooks/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import * as limitar from './limitar-agente.mjs';
import * as secretos from './proteger-secretos.mjs';

const RAIZ = path.resolve('/proyecto');
const escribir = (ruta) => ({ tool_name: 'Write', tool_input: { file_path: ruta } });
const ejecutar = (command, tool_name = 'Bash') => ({ tool_name, tool_input: { command } });
const permite = (agente, evento) => assert.equal(limitar.evaluar(agente, evento, RAIZ), null);
const bloquea = (agente, evento) => assert.notEqual(limitar.evaluar(agente, evento, RAIZ), null);

test('probador: solo escribe pruebas', () => {
  permite('probador', escribir('backend/tests/test_sitios.py'));
  permite('probador', escribir(path.join(RAIZ, 'backend', 'tests', 'conftest.py')));
  permite('probador', escribir('frontend/src/app/catalogo/catalogo.spec.ts'));
  bloquea('probador', escribir('backend/app/main.py'));
  bloquea('probador', escribir('frontend/src/app/catalogo/catalogo.ts'));
  bloquea('probador', escribir('specs/001-catalogo-sitios/tasks.md'));
  bloquea('probador', escribir('../otro-proyecto/backend/tests/x.py'));
});

test('implementador: escribe código pero no pruebas, docs ni .env', () => {
  permite('implementador', escribir('backend/app/main.py'));
  permite('implementador', escribir('frontend/src/app/catalogo/catalogo.ts'));
  bloquea('implementador', escribir('backend/tests/test_sitios.py'));
  bloquea('implementador', escribir('frontend/src/app/catalogo/catalogo.spec.ts'));
  bloquea('implementador', escribir('docs/ARNES.md'));
  bloquea('implementador', escribir('.claude/agents/implementador.md'));
  bloquea('implementador', escribir('backend/.env'));
  permite('implementador', escribir('backend/.env.example'));
});

test('curador-datos: solo backend/datos', () => {
  permite('curador-datos', escribir('backend/datos/sitios.json'));
  bloquea('curador-datos', escribir('backend/app/datos.py'));
});

test('comandos permitidos y bloqueados', () => {
  permite('probador', ejecutar('pytest backend/tests -q'));
  permite('probador', ejecutar('cd backend && python -m pytest -q'));
  permite('probador', ejecutar('npm test', 'PowerShell'));
  bloquea('probador', ejecutar('npm run build'));
  bloquea('probador', ejecutar('pytest; rm -rf backend'));
  bloquea('probador', ejecutar('pytest && git commit -m x'));
  bloquea('probador', ejecutar('pytest > salida.txt'));
  bloquea('probador', ejecutar('pytestx'));
  permite('implementador', ejecutar('npm run build'));
  bloquea('implementador', ejecutar('npm install leaflet'));
  bloquea('implementador', ejecutar('git commit -m "feat: x"'));
  bloquea('curador-datos', ejecutar('ls'));
});

test('registrador-prompts: solo docs/prompts y git de lectura', () => {
  permite('registrador-prompts', escribir('docs/prompts/002-2026-11-25-catalogo.md'));
  bloquea('registrador-prompts', escribir('docs/ARNES.md'));
  bloquea('registrador-prompts', escribir('backend/app/main.py'));
  permite('registrador-prompts', ejecutar('git log --oneline -20'));
  bloquea('registrador-prompts', ejecutar('git commit -m "docs: prompts"'));
  bloquea('registrador-prompts', ejecutar('git push'));
});

test('agente desconocido se bloquea', () => {
  bloquea('intruso', escribir('backend/app/main.py'));
});

test('proteger-secretos: archivos .env', () => {
  const lee = (ruta) => secretos.evaluar({ tool_name: 'Read', tool_input: { file_path: ruta } });
  assert.notEqual(lee('backend/.env'), null);
  assert.notEqual(lee('C:\\proyecto\\.env.local'), null);
  assert.equal(lee('backend/.env.example'), null);
  assert.equal(lee('backend/app/config.py'), null);
});

test('proteger-secretos: comandos', () => {
  const corre = (c) => secretos.evaluar(ejecutar(c));
  assert.notEqual(corre('cat backend/.env'), null);
  assert.notEqual(corre('Get-Content .env.local'), null);
  assert.equal(corre('cp backend/.env.example backend/.env.example.bak'), null);
  assert.equal(corre('cat .env.example'), null);
  assert.notEqual(corre('git push --force origin main'), null);
  assert.notEqual(corre('git push -f'), null);
  assert.notEqual(corre('git reset --hard HEAD~1'), null);
  assert.notEqual(corre('git add .'), null);
  assert.notEqual(corre('git add -A'), null);
  assert.equal(corre('git add backend/app/main.py'), null);
  assert.equal(corre('git push -u origin feat/001-catalogo-sitios'), null);
});
