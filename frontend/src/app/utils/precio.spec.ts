import { formatearPrecio, formatearPrecioReferencia } from './precio';

describe('formatearPrecio', () => {
  it('CA-2 formatea precio conocido', () => {
    expect(formatearPrecio(25000, '2026-11-24')).toBe('$25.000 COP (aprox., consultado en nov. 2026)');
  });

  it('CA-2 pone el punto como separador de miles', () => {
    expect(formatearPrecio(500, '2026-11-24')).toBe('$500 COP (aprox., consultado en nov. 2026)');
    expect(formatearPrecio(1250000, '2026-11-24')).toBe(
      '$1.250.000 COP (aprox., consultado en nov. 2026)',
    );
  });

  it('CA-2 abrevia los 12 meses', () => {
    const esperados = [
      'ene.', 'feb.', 'mar.', 'abr.', 'may.', 'jun.',
      'jul.', 'ago.', 'sept.', 'oct.', 'nov.', 'dic.',
    ];
    esperados.forEach((mes, i) => {
      const fecha = `2026-${String(i + 1).padStart(2, '0')}-15`;
      expect(formatearPrecio(10000, fecha)).toBe(`$10.000 COP (aprox., consultado en ${mes} 2026)`);
    });
  });

  it('CA-2 no cambia de mes por la zona horaria en los bordes del mes', () => {
    expect(formatearPrecio(10000, '2026-01-01')).toBe('$10.000 COP (aprox., consultado en ene. 2026)');
    expect(formatearPrecio(10000, '2026-12-31')).toBe('$10.000 COP (aprox., consultado en dic. 2026)');
  });

  it('CA-2 (R7) sin fecha de consulta no inventa la fecha', () => {
    expect(formatearPrecio(25000, null)).toBe('$25.000 COP (aprox.)');
  });

  it('CA-3 precio no disponible', () => {
    expect(formatearPrecio(null, null)).toBe('Precio no disponible');
    expect(formatearPrecio(null, '2026-11-24')).toBe('Precio no disponible');
    expect(formatearPrecio(null, null)).not.toContain('$0');
  });

  it('CA-4 gratis', () => {
    expect(formatearPrecio(0, '2026-11-24')).toBe('Gratis');
    expect(formatearPrecio(0, '2026-11-24')).not.toBe('Precio no disponible');
    expect(formatearPrecio(0, '2026-11-24')).not.toContain('$0');
  });
});

describe('formatearPrecioReferencia', () => {
  it('CA-3 precio no disponible cuando no hay referencia', () => {
    const texto = formatearPrecioReferencia(null);
    expect(texto).toBe('Precio no disponible');
    expect(texto).not.toContain('$0');
  });

  it('CA-2 con un solo precio no antepone Desde', () => {
    expect(
      formatearPrecioReferencia({ valor_cop: 25000, varios: false, fecha_referencia_precio: '2026-11-24' }),
    ).toBe('$25.000 COP (aprox., consultado en nov. 2026)');
  });

  it('CA-2 antepone Desde', () => {
    expect(
      formatearPrecioReferencia({ valor_cop: 15000, varios: true, fecha_referencia_precio: '2026-11-24' }),
    ).toBe('Desde $15.000 COP (aprox., consultado en nov. 2026)');
  });

  it('CA-4 gratis', () => {
    expect(
      formatearPrecioReferencia({ valor_cop: 0, varios: false, fecha_referencia_precio: '2026-11-24' }),
    ).toBe('Gratis');
  });

  it('CA-4 gratis con otras tarifas', () => {
    const texto = formatearPrecioReferencia({
      valor_cop: 0,
      varios: true,
      fecha_referencia_precio: '2026-11-24',
    });
    expect(texto).toBe('Gratis (hay otras tarifas)');
    expect(texto).not.toContain('Desde');
  });
});
