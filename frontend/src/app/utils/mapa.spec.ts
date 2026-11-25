import { urlOpenStreetMap } from './mapa';

describe('urlOpenStreetMap', () => {
  it('CA-7 arma la URL', () => {
    expect(urlOpenStreetMap(3.2333, -75.1667)).toBe(
      'https://www.openstreetmap.org/?mlat=3.2333&mlon=-75.1667#map=15/3.2333/-75.1667',
    );
  });

  it('CA-7 respeta los bordes del Huila', () => {
    expect(urlOpenStreetMap(1.5, -76.6)).toBe(
      'https://www.openstreetmap.org/?mlat=1.5&mlon=-76.6#map=15/1.5/-76.6',
    );
  });
});
