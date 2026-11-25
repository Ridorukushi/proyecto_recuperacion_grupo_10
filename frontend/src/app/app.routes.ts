import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'sitios', pathMatch: 'full' },
  {
    path: 'sitios',
    loadComponent: () => import('./pages/lista-sitios/lista-sitios').then((m) => m.ListaSitios),
  },
  {
    path: 'sitios/:slug',
    loadComponent: () => import('./pages/ficha-sitio/ficha-sitio').then((m) => m.FichaSitio),
  },
];
