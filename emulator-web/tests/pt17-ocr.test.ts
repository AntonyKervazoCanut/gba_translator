import { describe, expect, it } from 'vitest';
import { normalizePortugueseOcr } from '../../tests/e2e-playwright/helpers/pt17-ocr.js';

describe('OCR de la sonde PT-17', () => {
  it('reconnaît le a cyrillique produit par Vision pour le glyphe latin a', () => {
    const recognized = 'Bo\u0430 estratégia!';
    expect(normalizePortugueseOcr(recognized)).toBe('Boa estrategia!');
  });

  it('normalise accents et retours sans supprimer les mots du message', () => {
    const recognized = '  A conexão\n  caiu… ';
    expect(normalizePortugueseOcr(recognized)).toBe('A conexao caiu…');
  });

  it('conserve un texte anglais ou une véritable erreur de lettre', () => {
    expect(normalizePortugueseOcr('Good strategy!')).toBe('Good strategy!');
    expect(normalizePortugueseOcr('Boq estratégia!')).toBe('Boq estrategia!');
  });
});
