import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, TestRequest, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { ListaSitios } from './lista-sitios';

const TATACOA = {
  slug: 'desierto-de-la-tatacoa',
  nombre: 'Desierto de la Tatacoa',
  municipio: { clave: 'villavieja', etiqueta: 'Villavieja' },
  categoria: { clave: 'naturaleza', etiqueta: 'Naturaleza' },
  precio_referencia: { valor_cop: 15000, varios: true, fecha_referencia_precio: '2026-11-24' },
};
const BALNEARIO = {
  slug: 'balneario-termal-los-lagos',
  nombre: 'Balneario Termal Los Lagos',
  municipio: { clave: 'neiva', etiqueta: 'Neiva' },
  categoria: { clave: 'termales', etiqueta: 'Termales' },
  precio_referencia: null,
};
const MALECON = {
  slug: 'malecon-de-neiva',
  nombre: 'Malecón de Neiva',
  municipio: { clave: 'neiva', etiqueta: 'Neiva' },
  categoria: { clave: 'cultura', etiqueta: 'Cultura' },
  precio_referencia: { valor_cop: 0, varios: false, fecha_referencia_precio: '2026-11-24' },
};
const SANTUARIO = {
  slug: 'santuario-de-garzon',
  nombre: 'Santuario de Garzón',
  municipio: { clave: 'garzon', etiqueta: 'Garzón' },
  categoria: { clave: 'religioso', etiqueta: 'Religioso' },
  precio_referencia: { valor_cop: 0, varios: true, fecha_referencia_precio: '2026-11-24' },
};
const FILTROS = {
  municipios: [
    { clave: 'garzon', etiqueta: 'Garzón' },
    { clave: 'neiva', etiqueta: 'Neiva' },
    { clave: 'villavieja', etiqueta: 'Villavieja' },
  ],
  categorias: [
    { clave: 'cultura', etiqueta: 'Cultura' },
    { clave: 'naturaleza', etiqueta: 'Naturaleza' },
  ],
};

describe('ListaSitios', () => {
  let fixture: ComponentFixture<ListaSitios>;
  let http: HttpTestingController;

  const esLista = (r: TestRequest['request']) =>
    r.method === 'GET' && new URL(r.urlWithParams, 'http://x').pathname === '/api/sitios';
  const esFiltros = (r: TestRequest['request']) =>
    r.method === 'GET' && new URL(r.urlWithParams, 'http://x').pathname === '/api/filtros';
  const parametros = (t: TestRequest) => new URL(t.request.urlWithParams, 'http://x').searchParams;
  const pausa = () => new Promise<void>((resolver) => setTimeout(resolver, 0));
  const host = () => fixture.nativeElement as HTMLElement;
  const texto = () => host().textContent ?? '';

  /** Da vueltas al detector de cambios hasta que aparezcan peticiones que cumplan `condicion`. */
  async function esperarPeticiones(condicion: (r: TestRequest['request']) => boolean): Promise<TestRequest[]> {
    for (let i = 0; i < 100; i++) {
      fixture.detectChanges();
      const encontradas = http.match(condicion);
      if (encontradas.length > 0) return encontradas;
      await pausa();
    }
    throw new Error('La pantalla no hizo la petición esperada');
  }

  async function asentar(): Promise<void> {
    await pausa();
    fixture.detectChanges();
    await pausa();
    fixture.detectChanges();
  }

  /** Abre la pantalla y responde filtros y lista; devuelve cuando ya se pintó. */
  async function abrirConSitios(sitios: object[]): Promise<void> {
    fixture = TestBed.createComponent(ListaSitios);
    fixture.detectChanges();
    const lista = await esperarPeticiones(esLista);
    lista.forEach((t) => t.flush(sitios));
    http.match(esFiltros).forEach((t) => t.flush(FILTROS));
    await asentar();
    http.match(esFiltros).forEach((t) => t.flush(FILTROS));
    await asentar();
  }

  /** Busca el elemento más pequeño que contiene el texto y sube mientras siga conteniendo solo este sitio. */
  function tarjetaDe(nombre: string, todos: string[]): HTMLElement {
    const candidatos = Array.from(host().querySelectorAll<HTMLElement>('*')).filter((e) =>
      (e.textContent ?? '').includes(nombre),
    );
    expect(candidatos.length, `no aparece «${nombre}»`).toBeGreaterThan(0);
    let nodo = candidatos.reduce((a, b) => ((a.textContent ?? '').length <= (b.textContent ?? '').length ? a : b));
    const cuantos = (e: HTMLElement) => todos.filter((n) => (e.textContent ?? '').includes(n)).length;
    while (nodo.parentElement && nodo.parentElement !== host() && cuantos(nodo.parentElement) === 1) {
      nodo = nodo.parentElement;
    }
    return nodo;
  }

  function selectConOpcion(valor: string): HTMLSelectElement {
    const encontrado = Array.from(host().querySelectorAll('select')).find((s) =>
      Array.from(s.options).some((o) => o.value === valor),
    );
    expect(encontrado, `no hay un selector con la opción «${valor}»`).toBeTruthy();
    return encontrado as HTMLSelectElement;
  }

  function botonConTexto(patron: RegExp): HTMLElement {
    const encontrado = Array.from(host().querySelectorAll<HTMLElement>('button, a')).find((e) =>
      patron.test(e.textContent ?? ''),
    );
    expect(encontrado, `no hay un botón o enlace con ${patron}`).toBeTruthy();
    return encontrado as HTMLElement;
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    fixture?.destroy();
  });

  it('CA-1 muestra cada sitio con sus 4 datos', async () => {
    await abrirConSitios([BALNEARIO, TATACOA, MALECON, SANTUARIO]);
    const nombres = [BALNEARIO, TATACOA, MALECON, SANTUARIO].map((s) => s.nombre);

    const esperados: [{ nombre: string }, string, string, string][] = [
      [TATACOA, 'Villavieja', 'Naturaleza', 'Desde $15.000 COP (aprox., consultado en nov. 2026)'],
      [BALNEARIO, 'Neiva', 'Termales', 'Precio no disponible'],
      [MALECON, 'Neiva', 'Cultura', 'Gratis'],
      [SANTUARIO, 'Garzón', 'Religioso', 'Gratis (hay otras tarifas)'],
    ];
    for (const [sitio, municipio, categoria, precio] of esperados) {
      const tarjeta = tarjetaDe(sitio.nombre, nombres);
      const t = tarjeta.textContent ?? '';
      expect(t).toContain(sitio.nombre);
      expect(t).toContain(municipio);
      expect(t).toContain(categoria);
      expect(t).toContain(precio);
    }
    // El de entrada gratuita sin otras tarifas no dice «Precio no disponible» ni «Desde».
    const gratis = tarjetaDe(MALECON.nombre, nombres).textContent ?? '';
    expect(gratis).not.toContain('Precio no disponible');
    expect(gratis).not.toContain('Gratis (hay otras tarifas)');
    expect(gratis).not.toContain('Desde');
    // CA-3: ningún «$0».
    expect(texto()).not.toContain('$0');
  });

  it('CA-1 respeta el orden que entrega la API y enlaza a la ficha', async () => {
    await abrirConSitios([BALNEARIO, TATACOA, MALECON]);
    const t = texto();
    expect(t.indexOf(BALNEARIO.nombre)).toBeGreaterThanOrEqual(0);
    expect(t.indexOf(BALNEARIO.nombre)).toBeLessThan(t.indexOf(TATACOA.nombre));
    expect(t.indexOf(TATACOA.nombre)).toBeLessThan(t.indexOf(MALECON.nombre));
    const enlace = host().querySelector('a[href$="/sitios/desierto-de-la-tatacoa"]');
    expect(enlace).toBeTruthy();
  });

  it('CA-5 carga', async () => {
    fixture = TestBed.createComponent(ListaSitios);
    fixture.detectChanges();
    const lista = await esperarPeticiones(esLista);
    expect(texto()).toMatch(/cargando/i);
    expect(texto()).not.toContain('No hay sitios para mostrar');
    lista.forEach((t) => t.flush([TATACOA]));
    http.match(esFiltros).forEach((t) => t.flush(FILTROS));
    await asentar();
    expect(texto()).not.toMatch(/cargando/i);
    expect(texto()).toContain('Desierto de la Tatacoa');
  });

  it('CA-5 vacío', async () => {
    await abrirConSitios([]);
    expect(texto()).toContain('No hay sitios para mostrar');
    expect(texto()).not.toContain('No hay sitios que coincidan con tu búsqueda');
    expect(texto()).not.toMatch(/cargando/i);
  });

  it('CA-5 error y reintentar', async () => {
    fixture = TestBed.createComponent(ListaSitios);
    fixture.detectChanges();
    const lista = await esperarPeticiones(esLista);
    lista.forEach((t) => t.flush('fallo', { status: 500, statusText: 'Server Error' }));
    http.match(esFiltros).forEach((t) => t.flush(FILTROS));
    await asentar();

    expect(texto()).toMatch(/no se pudo|error/i);
    expect(texto()).not.toContain('No hay sitios para mostrar');
    expect(texto()).not.toContain('Http failure');

    botonConTexto(/reintentar/i).click();
    const nueva = await esperarPeticiones(esLista);
    nueva.forEach((t) => t.flush([TATACOA]));
    await asentar();
    expect(texto()).toContain('Desierto de la Tatacoa');
    expect(texto()).not.toMatch(/reintentar/i);
  });

  it('CA-14 sin resultados y limpiar', async () => {
    await abrirConSitios([TATACOA, BALNEARIO]);

    // El turista elige el municipio «Neiva»: la API no devuelve nada para esa combinación.
    const selector = selectConOpcion('neiva');
    selector.value = 'neiva';
    selector.dispatchEvent(new Event('change', { bubbles: true }));
    const filtrada = await esperarPeticiones((r) => esLista(r) && new URL(r.urlWithParams, 'http://x').searchParams.get('municipio') === 'neiva');
    expect(parametros(filtrada[0]).get('municipio')).toBe('neiva');
    filtrada.forEach((t) => t.flush([]));
    await asentar();

    expect(texto()).toContain('No hay sitios que coincidan con tu búsqueda');
    expect(texto()).not.toContain('No hay sitios para mostrar');
    const limpiar = botonConTexto(/Limpiar filtros/);

    limpiar.click();
    const sinFiltro = await esperarPeticiones((r) => esLista(r) && !new URL(r.urlWithParams, 'http://x').searchParams.has('municipio'));
    sinFiltro.forEach((t) => t.flush([TATACOA, BALNEARIO]));
    await asentar();

    expect(texto()).not.toContain('No hay sitios que coincidan con tu búsqueda');
    expect(texto()).toContain('Desierto de la Tatacoa');
    expect(texto()).toContain('Balneario Termal Los Lagos');
    expect(selectConOpcion('neiva').value).toBe('');
  });

  it('CA-10 ofrece los municipios y categorías que entrega la API', async () => {
    await abrirConSitios([TATACOA]);
    const municipios = selectConOpcion('neiva');
    const categorias = selectConOpcion('cultura');
    expect(Array.from(municipios.options).map((o) => o.textContent?.trim())).toEqual(
      expect.arrayContaining(['Garzón', 'Neiva', 'Villavieja']),
    );
    expect(Array.from(categorias.options).map((o) => o.textContent?.trim())).toEqual(
      expect.arrayContaining(['Cultura', 'Naturaleza']),
    );
  });
});
