import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, TestRequest, provideHttpClientTesting } from '@angular/common/http/testing';
import { firstValueFrom, from } from 'rxjs';
import { SitiosService } from './sitios.service';

describe('SitiosService', () => {
  let servicio: SitiosService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    servicio = TestBed.inject(SitiosService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  /** Espera una petición GET a la ruta dada (sin importar cómo arme la consulta) y devuelve sus parámetros. */
  function esperar(ruta: string): { req: TestRequest; params: URLSearchParams } {
    const req = http.expectOne((r) => r.method === 'GET' && new URL(r.urlWithParams, 'http://x').pathname === ruta);
    return { req, params: new URL(req.request.urlWithParams, 'http://x').searchParams };
  }

  it('CA-10 envía municipio', async () => {
    const resultado = firstValueFrom(from(servicio.listar({ municipio: 'neiva' })));
    const { req, params } = esperar('/api/sitios');
    expect(params.get('municipio')).toBe('neiva');
    expect(params.has('categoria')).toBe(false);
    expect(params.has('q')).toBe(false);
    req.flush([]);
    expect(await resultado).toEqual([]);
  });

  it('CA-13 envía los tres filtros', async () => {
    const resultado = firstValueFrom(
      from(servicio.listar({ municipio: 'villavieja', categoria: 'cultura', q: 'cañón y río' })),
    );
    const { req, params } = esperar('/api/sitios');
    expect(params.get('municipio')).toBe('villavieja');
    expect(params.get('categoria')).toBe('cultura');
    expect(params.get('q')).toBe('cañón y río');
    req.flush([]);
    await resultado;
  });

  it('CA-1 sin filtros pide la lista sin parámetros y devuelve lo que responde la API', async () => {
    const sitios = [
      {
        slug: 'desierto-de-la-tatacoa',
        nombre: 'Desierto de la Tatacoa',
        municipio: { clave: 'villavieja', etiqueta: 'Villavieja' },
        categoria: { clave: 'naturaleza', etiqueta: 'Naturaleza' },
        precio_referencia: { valor_cop: 15000, varios: true, fecha_referencia_precio: '2026-11-24' },
      },
    ];
    const resultado = firstValueFrom(from(servicio.listar({})));
    const { req, params } = esperar('/api/sitios');
    expect([...params.keys()]).toEqual([]);
    req.flush(sitios);
    expect(await resultado).toEqual(sitios);
  });

  it('CA-7 (spec 002) listar con orden precio envía orden=precio', async () => {
    const resultado = firstValueFrom(from(servicio.listar({ orden: 'precio' } as never)));
    const { req, params } = esperar('/api/sitios');
    expect(params.get('orden')).toBe('precio');
    req.flush([]);
    await resultado;
  });

  it('CA-7 (spec 002) listar con orden nombre no envía el parámetro orden', async () => {
    const resultado = firstValueFrom(from(servicio.listar({ orden: 'nombre' } as never)));
    const { req, params } = esperar('/api/sitios');
    expect(params.has('orden')).toBe(false);
    req.flush([]);
    await resultado;
  });

  it('CA-20 obtener pide la ficha por slug', async () => {
    const resultado = firstValueFrom(from(servicio.obtener('desierto-de-la-tatacoa')));
    const { req } = esperar('/api/sitios/desierto-de-la-tatacoa');
    req.flush({ slug: 'desierto-de-la-tatacoa', nombre: 'Desierto de la Tatacoa' });
    expect((await resultado).nombre).toBe('Desierto de la Tatacoa');
  });

  it('CA-9 propaga el error 404 de una ficha inexistente', async () => {
    const resultado = firstValueFrom(from(servicio.obtener('sitio-que-no-existe')));
    const { req } = esperar('/api/sitios/sitio-que-no-existe');
    req.flush({ detalle: 'Sitio no encontrado.' }, { status: 404, statusText: 'Not Found' });
    await expect(resultado).rejects.toMatchObject({ status: 404 });
  });

  it('CA-10 filtros pide municipios y categorías', async () => {
    const respuesta = {
      municipios: [{ clave: 'neiva', etiqueta: 'Neiva' }],
      categorias: [{ clave: 'cultura', etiqueta: 'Cultura' }],
    };
    const resultado = firstValueFrom(from(servicio.filtros()));
    const { req } = esperar('/api/filtros');
    req.flush(respuesta);
    expect(await resultado).toEqual(respuesta);
  });
});
