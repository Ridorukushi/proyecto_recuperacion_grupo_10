import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, TestRequest, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router, provideRouter, withComponentInputBinding } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { FichaSitio } from './ficha-sitio';

const TATACOA = {
  slug: 'desierto-de-la-tatacoa',
  nombre: 'Desierto de la Tatacoa',
  municipio: { clave: 'villavieja', etiqueta: 'Villavieja' },
  categoria: { clave: 'naturaleza', etiqueta: 'Naturaleza' },
  descripcion: 'Zona árida de prueba con cielos despejados.',
  latitud: 3.2333,
  longitud: -75.1667,
  horario: 'Todos los días, 24 horas',
  como_llegar: 'Por la vía Neiva - Villavieja.',
  precios: [
    { concepto: 'Entrada adulto', valor_cop: 25000 },
    { concepto: 'Entrada niño', valor_cop: 15000 },
  ],
  fecha_referencia_precio: '2026-11-24',
  fuentes: ['https://example.org/tatacoa-a', 'https://example.org/tatacoa-b'],
};

const SIN_DATOS = {
  slug: 'balneario-termal-los-lagos',
  nombre: 'Balneario Termal Los Lagos',
  municipio: { clave: 'neiva', etiqueta: 'Neiva' },
  categoria: { clave: 'termales', etiqueta: 'Termales' },
  descripcion: null,
  latitud: 2.93,
  longitud: -75.28,
  horario: null,
  como_llegar: null,
  precios: [],
  fecha_referencia_precio: null,
  fuentes: ['https://example.org/balneario'],
};

describe('FichaSitio', () => {
  let http: HttpTestingController;
  let harness: RouterTestingHarness;

  const pausa = () => new Promise<void>((resolver) => setTimeout(resolver, 0));
  const host = () => harness.routeNativeElement as HTMLElement;
  const texto = () => host().textContent ?? '';
  const aparece = (texto_: string, parte: string) => texto_.split(parte).length - 1;

  async function esperarFicha(slug: string): Promise<TestRequest> {
    const condicion = (r: TestRequest['request']) =>
      r.method === 'GET' && new URL(r.urlWithParams, 'http://x').pathname === `/api/sitios/${slug}`;
    for (let i = 0; i < 100; i++) {
      harness.detectChanges();
      const encontradas = http.match(condicion);
      if (encontradas.length > 0) return encontradas[0];
      await pausa();
    }
    throw new Error(`La ficha no pidió /api/sitios/${slug}`);
  }

  /** Abre /sitios/<slug> con el enrutador real y responde la petición con `cuerpo` (o con un error). */
  async function abrir(
    slug: string,
    respuesta: object,
    opciones?: { status: number; statusText: string },
  ): Promise<void> {
    await harness.navigateByUrl(`/sitios/${slug}`, FichaSitio);
    const peticion = await esperarFicha(slug);
    peticion.flush(respuesta, opciones);
    await pausa();
    harness.detectChanges();
    await pausa();
    harness.detectChanges();
  }

  beforeEach(async () => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'sitios/:slug', component: FichaSitio }], withComponentInputBinding()),
      ],
    });
    http = TestBed.inject(HttpTestingController);
    harness = await RouterTestingHarness.create();
  });

  it('CA-6 muestra la ficha completa', async () => {
    await abrir('desierto-de-la-tatacoa', TATACOA);
    const t = texto();
    expect(t).toContain('Desierto de la Tatacoa');
    expect(t).toContain('Villavieja');
    expect(t).toContain('Naturaleza');
    expect(t).toContain('Zona árida de prueba con cielos despejados.');
    expect(t).toContain('Entrada adulto');
    expect(t).toContain('$25.000 COP (aprox., consultado en nov. 2026)');
    expect(t).toContain('Entrada niño');
    expect(t).toContain('$15.000 COP (aprox., consultado en nov. 2026)');
    expect(t).not.toContain('Desde'); // en la ficha cada precio va con su concepto, sin «Desde»
    expect(t).toContain('Todos los días, 24 horas');
    expect(t).toContain('Por la vía Neiva - Villavieja.');
    expect(t).not.toContain('No disponible');
    expect(t).not.toContain('Precio no disponible');
  });

  it('CA-6 las fuentes son enlaces que abren en pestaña nueva', async () => {
    await abrir('desierto-de-la-tatacoa', TATACOA);
    for (const url of TATACOA.fuentes) {
      const enlace = host().querySelector<HTMLAnchorElement>(`a[href="${url}"]`);
      expect(enlace, `falta el enlace a ${url}`).toBeTruthy();
      expect(enlace?.getAttribute('target')).toBe('_blank');
      expect(enlace?.getAttribute('rel')).toContain('noopener');
    }
  });

  it('CA-7 enlace Ver en mapa', async () => {
    await abrir('desierto-de-la-tatacoa', TATACOA);
    const enlace = Array.from(host().querySelectorAll<HTMLAnchorElement>('a')).find((a) =>
      /Ver en mapa/i.test(a.textContent ?? ''),
    );
    expect(enlace, 'falta el enlace «Ver en mapa»').toBeTruthy();
    expect(enlace?.getAttribute('href')).toBe(
      'https://www.openstreetmap.org/?mlat=3.2333&mlon=-75.1667#map=15/3.2333/-75.1667',
    );
    expect(enlace?.getAttribute('target')).toBe('_blank');
    expect(enlace?.getAttribute('rel')).toContain('noopener');
  });

  it('CA-8 No disponible', async () => {
    await abrir('balneario-termal-los-lagos', SIN_DATOS);
    const t = texto();
    expect(t).toContain('Balneario Termal Los Lagos');
    expect(aparece(t, 'No disponible')).toBeGreaterThanOrEqual(2); // horario y cómo llegar
    expect(t).toContain('Precio no disponible');
    expect(t).not.toContain('$0');
    expect(t).not.toContain('null');
    expect(t).not.toContain('undefined');
  });

  it('CA-8 solo el campo desconocido dice No disponible', async () => {
    await abrir('desierto-de-la-tatacoa', { ...TATACOA, como_llegar: null });
    const t = texto();
    expect(t).toContain('Todos los días, 24 horas');
    expect(aparece(t, 'No disponible')).toBe(1);
  });

  it('CA-4 muestra Gratis y no Precio no disponible cuando el precio es 0', async () => {
    await abrir('malecon-de-neiva', {
      ...SIN_DATOS,
      slug: 'malecon-de-neiva',
      nombre: 'Malecón de Neiva',
      precios: [{ concepto: 'Entrada', valor_cop: 0 }],
      fecha_referencia_precio: '2026-11-24',
    });
    const t = texto();
    expect(t).toContain('Entrada');
    expect(t).toContain('Gratis');
    expect(t).not.toContain('Precio no disponible');
    expect(t).not.toContain('$0');
  });

  it('CA-9 no encontrado', async () => {
    await abrir(
      'sitio-que-no-existe',
      { detalle: 'Sitio no encontrado.' },
      { status: 404, statusText: 'Not Found' },
    );
    expect(texto()).toContain('Sitio no encontrado');
    const volver = host().querySelector<HTMLAnchorElement>('a[href="/sitios"]');
    expect(volver, 'falta el enlace para volver a la lista (/sitios)').toBeTruthy();
    expect(texto()).not.toContain('Villavieja');
  });

  it('CA-20 carga el sitio del parámetro slug', async () => {
    await abrir('desierto-de-la-tatacoa', TATACOA);
    expect(TestBed.inject(Router).url).toBe('/sitios/desierto-de-la-tatacoa');
    expect(texto()).toContain('Desierto de la Tatacoa');
  });

  it('CA-20 pide a la API el slug que viene en la dirección, no uno fijo', async () => {
    await abrir('parque-arqueologico-de-san-agustin', {
      ...SIN_DATOS,
      slug: 'parque-arqueologico-de-san-agustin',
      nombre: 'Parque Arqueológico de San Agustín',
      municipio: { clave: 'san-agustin', etiqueta: 'San Agustín' },
      categoria: { clave: 'arqueologia', etiqueta: 'Arqueología' },
    });
    expect(texto()).toContain('Parque Arqueológico de San Agustín');
    expect(texto()).not.toContain('Desierto de la Tatacoa');
  });
});
