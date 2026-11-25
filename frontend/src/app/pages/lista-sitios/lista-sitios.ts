import { ChangeDetectionStrategy, Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { Filtros, SitioResumen } from '../../models/sitio';
import { SitiosService } from '../../services/sitios.service';
import { formatearPrecioReferencia } from '../../utils/precio';

type Estado = 'cargando' | 'listo' | 'error';

const ESPERA_BUSQUEDA_MS = 300;

@Component({
  selector: 'app-lista-sitios',
  imports: [RouterLink],
  templateUrl: './lista-sitios.html',
  styleUrl: './lista-sitios.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ListaSitios {
  private readonly servicio = inject(SitiosService);
  private readonly router = inject(Router);
  private readonly ruta = inject(ActivatedRoute);

  private pendiente?: Subscription;
  private temporizador?: ReturnType<typeof setTimeout>;

  protected readonly estado = signal<Estado>('cargando');
  protected readonly filtros = signal<Filtros>({ municipios: [], categorias: [] });
  protected readonly municipio = signal('');
  protected readonly categoria = signal('');
  protected readonly q = signal('');

  protected readonly errorFiltros = signal(false);
  /** Mensaje del servidor cuando responde 422 (filtros inválidos); vacío en otros errores. */
  protected readonly detalleError = signal('');

  protected readonly tarjetas = signal<SitioResumen[]>([]);
  protected readonly hayFiltros = computed(() => !!(this.municipio() || this.categoria() || this.q().trim()));

  protected readonly precioDe = formatearPrecioReferencia;

  constructor() {
    const parametros = this.ruta.snapshot.queryParamMap;
    this.municipio.set(parametros.get('municipio') ?? '');
    this.categoria.set(parametros.get('categoria') ?? '');
    this.q.set(parametros.get('q') ?? '');

    inject(DestroyRef).onDestroy(() => {
      this.pendiente?.unsubscribe();
      clearTimeout(this.temporizador);
    });
    // Si los filtros no cargan, la lista sigue funcionando sin los selectores.
    this.servicio
      .filtros()
      .pipe(takeUntilDestroyed())
      .subscribe({ next: (f) => this.filtros.set(f), error: () => this.errorFiltros.set(true) });
    this.cargar();
  }

  protected elegirMunicipio(evento: Event): void {
    this.municipio.set((evento.target as HTMLSelectElement).value);
    this.cargar();
  }

  protected elegirCategoria(evento: Event): void {
    this.categoria.set((evento.target as HTMLSelectElement).value);
    this.cargar();
  }

  /** La búsqueda por texto espera 300 ms sin teclear antes de pedir la lista. */
  protected escribir(evento: Event): void {
    this.q.set((evento.target as HTMLInputElement).value);
    clearTimeout(this.temporizador);
    this.temporizador = setTimeout(() => this.cargar(), ESPERA_BUSQUEDA_MS);
  }

  protected limpiar(): void {
    this.municipio.set('');
    this.categoria.set('');
    this.q.set('');
    this.cargar();
  }

  protected cargar(): void {
    clearTimeout(this.temporizador);
    this.pendiente?.unsubscribe();
    this.estado.set('cargando');
    const filtros = { municipio: this.municipio(), categoria: this.categoria(), q: this.q() };
    void this.router.navigate([], {
      relativeTo: this.ruta,
      queryParams: {
        municipio: filtros.municipio || null,
        categoria: filtros.categoria || null,
        q: filtros.q.trim() || null,
      },
      replaceUrl: true,
    });
    this.pendiente = this.servicio.listar(filtros).subscribe({
      next: (sitios) => {
        this.tarjetas.set(sitios);
        this.estado.set('listo');
      },
      error: (error: unknown) => {
        const detalle = (error as { status?: number; error?: { detalle?: unknown } }) ?? {};
        this.detalleError.set(
          detalle.status === 422 && typeof detalle.error?.detalle === 'string' ? detalle.error.detalle : '',
        );
        this.estado.set('error');
      },
    });
  }
}
