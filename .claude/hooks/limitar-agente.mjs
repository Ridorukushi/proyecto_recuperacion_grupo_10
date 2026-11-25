#!/usr/bin/env node
// Hook PreToolUse de los subagentes probador, implementador y curador-datos.
// Hace cumplir en qué carpetas puede escribir cada agente y qué comandos puede ejecutar.
// Uso: node limitar-agente.mjs <agente>  (recibe por stdin el JSON del evento de Claude Code)
// Salida: código 0 = permitido; código 2 = bloqueado (el motivo va por stderr y lo lee el agente).

import path from 'node:path';

const ES_PRUEBA = (r) => r.startsWith('backend/tests/') || (r.startsWith('frontend/src/') && r.endsWith('.spec.ts'));

const COMANDOS_PRUEBA = [
  'pytest',
  'python -m pytest',
  'uv run pytest',
  'npm test',
  'npm run test',
  'npx ng test',
  'npx vitest run',
];

export const POLITICAS = {
  probador: {
    puedeEscribir: (r) => ES_PRUEBA(r),
    descripcionEscritura: 'solo backend/tests/** y frontend/src/**/*.spec.ts',
    comandos: COMANDOS_PRUEBA,
  },
  implementador: {
    puedeEscribir: (r) => (r.startsWith('backend/') || r.startsWith('frontend/')) && !ES_PRUEBA(r),
    descripcionEscritura: 'backend/** y frontend/** sin las pruebas',
    comandos: [
      ...COMANDOS_PRUEBA,
      'npm run build',
      'npm run lint',
      'npx ng build',
      'ruff check',
      'python -m ruff check',
      'uv run ruff check',
    ],
  },
  'curador-datos': {
    puedeEscribir: (r) => r.startsWith('backend/datos/'),
    descripcionEscritura: 'solo backend/datos/**',
    comandos: [],
  },
  'registrador-prompts': {
    puedeEscribir: (r) => r.startsWith('docs/prompts/'),
    descripcionEscritura: 'solo docs/prompts/**',
    comandos: ['git log', 'git status', 'git show --stat'],
  },
};

const HERRAMIENTAS_ESCRITURA = new Set(['Edit', 'Write', 'MultiEdit', 'NotebookEdit']);
const HERRAMIENTAS_COMANDO = new Set(['Bash', 'PowerShell']);

/** Convierte una ruta del evento en ruta relativa al proyecto con barras '/'. null si queda fuera. */
export function rutaRelativa(ruta, raiz) {
  const absoluta = path.resolve(raiz, ruta);
  const relativa = path.relative(raiz, absoluta).split(path.sep).join('/');
  if (relativa === '' || relativa.startsWith('..') || path.isAbsolute(relativa)) return null;
  return relativa;
}

export function esArchivoEnv(relativa) {
  const nombre = relativa.split('/').pop() ?? '';
  return /^\.env(\..+)?$/.test(nombre) && nombre !== '.env.example';
}

/** Quita un único prefijo "cd backend && " o "cd frontend && " (o "; " en PowerShell). */
function quitarCd(comando) {
  return comando.replace(/^cd\s+["']?(backend|frontend)["']?\s*(&&|;)\s*/, '');
}

export function comandoPermitido(comando, permitidos) {
  const limpio = quitarCd(comando.trim());
  if (/[;&|<>`]|\$\(/.test(limpio)) return false; // sin encadenar, redirigir ni sustituir
  return permitidos.some((p) => limpio === p || limpio.startsWith(p + ' '));
}

/** Devuelve null si se permite, o el motivo del bloqueo. */
export function evaluar(agente, evento, raiz) {
  const politica = POLITICAS[agente];
  if (!politica) return `Agente desconocido para limitar-agente: "${agente}".`;
  const herramienta = evento.tool_name;
  const entrada = evento.tool_input ?? {};

  if (HERRAMIENTAS_ESCRITURA.has(herramienta)) {
    const ruta = entrada.file_path ?? entrada.notebook_path;
    if (!ruta) return 'No se pudo determinar el archivo a modificar.';
    const relativa = rutaRelativa(ruta, raiz);
    if (!relativa) return `El ${agente} no puede escribir fuera del proyecto (${ruta}).`;
    if (esArchivoEnv(relativa)) return `Ningún agente puede modificar ${relativa}.`;
    if (!politica.puedeEscribir(relativa)) {
      return `El ${agente} no puede escribir en ${relativa}: ${politica.descripcionEscritura}.`;
    }
    return null;
  }

  if (HERRAMIENTAS_COMANDO.has(herramienta)) {
    const comando = String(entrada.command ?? '');
    if (!comandoPermitido(comando, politica.comandos)) {
      const lista = politica.comandos.length ? politica.comandos.join(', ') : 'ninguno';
      return `El ${agente} no puede ejecutar "${comando}". Comandos permitidos: ${lista}.`;
    }
    return null;
  }

  return null;
}

async function leerEntrada() {
  let datos = '';
  for await (const trozo of process.stdin) datos += trozo;
  return datos;
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('limitar-agente.mjs')) {
  const agente = process.argv[2] ?? '';
  let evento;
  try {
    evento = JSON.parse(await leerEntrada());
  } catch {
    process.stderr.write('limitar-agente: no se pudo leer el evento.\n');
    process.exit(2);
  }
  const raiz = process.env.CLAUDE_PROJECT_DIR || evento.cwd || process.cwd();
  const motivo = evaluar(agente, evento, raiz);
  if (motivo) {
    process.stderr.write(motivo + '\n');
    process.exit(2);
  }
  process.exit(0);
}
