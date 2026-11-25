/** Enlace a OpenStreetMap centrado en las coordenadas del sitio. */
export function urlOpenStreetMap(latitud: number, longitud: number): string {
  return `https://www.openstreetmap.org/?mlat=${latitud}&mlon=${longitud}#map=15/${latitud}/${longitud}`;
}
