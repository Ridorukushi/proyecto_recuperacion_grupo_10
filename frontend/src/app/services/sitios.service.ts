import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Filtros, FiltrosLista, SitioDetalle, SitioResumen } from '../models/sitio';

const API = '/api';

@Injectable({ providedIn: 'root' })
export class SitiosService {
  private readonly http = inject(HttpClient);

  listar(filtros: FiltrosLista): Observable<SitioResumen[]> {
    let params = new HttpParams();
    if (filtros.municipio) params = params.set('municipio', filtros.municipio);
    if (filtros.categoria) params = params.set('categoria', filtros.categoria);
    if (filtros.q?.trim()) params = params.set('q', filtros.q);
    return this.http.get<SitioResumen[]>(`${API}/sitios`, { params });
  }

  obtener(slug: string): Observable<SitioDetalle> {
    return this.http.get<SitioDetalle>(`${API}/sitios/${encodeURIComponent(slug)}`);
  }

  filtros(): Observable<Filtros> {
    return this.http.get<Filtros>(`${API}/filtros`);
  }
}
