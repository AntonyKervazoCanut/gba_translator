import { describe, expect, it } from 'vitest';
import { hasPortugueseOcrLines } from '../../tests/e2e-playwright/helpers/pt51-ocr.js';

describe('Lectures OCR de la sonde PT-51', () => {
  const line = 'Quando Reuniclus dão as mãos,';

  it('accepte la lecture correcte à un autre zoom sans corriger la lecture erronée', () => {
    const readings = ['Quando Reuniolus dão as mãos,', 'quando reuniclus dao as maos,'];
    expect(hasPortugueseOcrLines(readings, [line])).toBe(true);
  });

  it('rejette une véritable erreur de lettre et un texte resté anglais', () => {
    expect(hasPortugueseOcrLines(['Quando Reuniolus dão as mãos,'], [line])).toBe(false);
    expect(hasPortugueseOcrLines(['When Reuniclus shake hands,'], [line])).toBe(false);
  });

  it('ne reconstitue pas artificiellement une ligne avec deux lectures partielles', () => {
    expect(hasPortugueseOcrLines(['Quando Reuniclus', 'dão as mãos,'], [line])).toBe(false);
  });

  it('exige toutes les lignes attendues et une attente non vide', () => {
    expect(hasPortugueseOcrLines([line], [line, 'uma rede liga seus cérebros'])).toBe(false);
    expect(hasPortugueseOcrLines([line], [])).toBe(false);
    expect(hasPortugueseOcrLines([line], [''])).toBe(false);
  });
});
