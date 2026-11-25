#!/usr/bin/env node
// Hook PreToolUse de la sesión principal y de todos los subagentes.
// Bloquea leer, editar o mostrar archivos .env (salvo .env.example) y los comandos git peligrosos.
// Salida: código 0 = permitido; código 2 = bloqueado (el motivo va por stderr).

const HERRAMIENTAS_ARCHIVO = new Set(['Read', 'Edit', 'Write', 'MultiEdit', 'NotebookEdit']);
const HERRAMIENTAS_COMANDO = new Set(['Bash', 'PowerShell']);

export function esArchivoEnv(ruta) {
  const nombre = String(ruta).split(/[\\/]/).pop() ?? '';
  return /^\.env(\..+)?$/.test(nombre) && nombre !== '.env.example';
}

/** true si el comando menciona un archivo .env distinto de .env.example. */
export function comandoTocaEnv(comando) {
  const menciones = comando.match(/(^|[\s"'=\\/])\.env(\.[\w.-]+)?(?=$|[\s"';|&)>])/g) ?? [];
  return menciones.some((m) => !m.trim().replace(/^["'=\\/]/, '').startsWith('.env.example'));
}

const GIT_PROHIBIDO = [
  [/\bgit\s+push\b[^\n]*\s(--force(-with-lease)?|-f)\b/, 'git push --force está prohibido.'],
  [/\bgit\s+reset\s+--hard\b/, 'git reset --hard está prohibido.'],
  [/\bgit\s+add\s+(\.|-A|--all)(\s|$)/, 'Agrega los archivos por su ruta: nunca git add . ni git add -A.'],
];

/** Devuelve null si se permite, o el motivo del bloqueo. */
export function evaluar(evento) {
  const herramienta = evento.tool_name;
  const entrada = evento.tool_input ?? {};

  if (HERRAMIENTAS_ARCHIVO.has(herramienta)) {
    const ruta = entrada.file_path ?? entrada.notebook_path ?? '';
    if (esArchivoEnv(ruta)) return `Los archivos .env no se leen ni se editan (${ruta}). Usa .env.example.`;
    return null;
  }

  if (HERRAMIENTAS_COMANDO.has(herramienta)) {
    const comando = String(entrada.command ?? '');
    if (comandoTocaEnv(comando)) return 'El comando toca un archivo .env: no está permitido.';
    for (const [patron, motivo] of GIT_PROHIBIDO) if (patron.test(comando)) return motivo;
  }
  return null;
}

async function leerEntrada() {
  let datos = '';
  for await (const trozo of process.stdin) datos += trozo;
  return datos;
}

if (process.argv[1]?.endsWith('proteger-secretos.mjs')) {
  let evento;
  try {
    evento = JSON.parse(await leerEntrada());
  } catch {
    process.exit(0); // sin evento legible no hay nada que proteger
  }
  const motivo = evaluar(evento);
  if (motivo) {
    process.stderr.write(motivo + '\n');
    process.exit(2);
  }
  process.exit(0);
}
