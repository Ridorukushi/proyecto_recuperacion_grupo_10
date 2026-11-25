import { ChangeDetectionStrategy, Component, DestroyRef, computed, effect, inject, input, signal, untracked } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { SitioDetalle } from '../../models/sitio';
import { SitiosService } from '../../services/sitios.service';
import { urlOpenStreetMap } from '../../utils/mapa';
import { formatearPrecio } from '../../utils/precio';

type Estado = 'cargando' | 'listo' | 'no-encontrado' | 'error';

@Component({
  selector: 'app-ficha-sitio',
  imports: [RouterLink],
  templateUrl: './ficha-sitio.html',
  styleUrl: './ficha-sitio.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FichaSitio {
  /** Parámetro `:slug` de la ruta (llega por withComponentInputBinding). */
  readonly slug = input.required<string>();

  private readonly servicio = inject(SitiosService);
  private pendiente?: Subscription;

  protected readonly estado = signal<Estado>('cargando');
  protected readonly sitio = signal<SitioDetalle | null>(null);

  protected readonly precios = computed(() => {
    const sitio = this.sitio();
    if (!sitio) return [];
    return sitio.precios.map((p) => ({
      concepto: p.concepto,
      texto: formatearPrecio(p.valor_cop, sitio.fecha_referencia_precio),
    }));
  });

  protected readonly urlMapa = computed(() => {
    const sitio = this.sitio();
    return sitio ? urlOpenStreetMap(sitio.latitud, sitio.longitud) : '';
  });

  constructor() {
    inject(DestroyRef).onDestroy(() => this.pendiente?.unsubscribe());
    effect(() => {
      const slug = this.slug();
      untracked(() => this.cargar(slug));
    });
  }

  protected reintentar(): void {
    this.cargar(this.slug());
  }

  private cargar(slug: string): void {
    this.pendiente?.unsubscribe();
    this.estado.set('cargando');
    this.sitio.set(null);
    this.pendiente = this.servicio.obtener(slug).subscribe({
      next: (sitio) => {
        this.sitio.set(sitio);
        this.estado.set('listo');
      },
      error: (error: unknown) =>
        this.estado.set(error instanceof HttpErrorResponse && error.status === 404 ? 'no-encontrado' : 'error'),
    });
  }
}
