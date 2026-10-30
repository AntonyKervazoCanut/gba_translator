import { describe, expect, it } from 'vitest';
import { matchesPortugueseOcrLine } from '../../tests/e2e-playwright/helpers/pt49-ocr.js';

describe('Lecture des lignes de descriptions PT-49 dans Vision', () => {
  it('accepte la casse et les accents reconnus différemment', () => {
    expect(matchesPortugueseOcrLine('Permite sua Megaevolucao', 'Permite sua Megaevolução')).toBe(true);
  });
  it('tolère une seule confusion A/H ou a/g', () => {
    expect(matchesPortugueseOcrLine('Ho segurar', 'Ao segurar')).toBe(true);
    expect(matchesPortugueseOcrLine('Meggevolução', 'Megaevolução')).toBe(true);
  });
  it('rejette une ligne tronquée ou un mot absent', () => {
    expect(matchesPortugueseOcrLine('movimento desse tipo', 'movimento desse tipo uma vez.')).toBe(false);
  });
  it('rejette deux caractères erronés', () => {
    expect(matchesPortugueseOcrLine('Ho segurgr', 'Ao segurar')).toBe(false);
  });
  it('rejette des lignes fusionnées et une ligne vide', () => {
    expect(matchesPortugueseOcrLine('ser segurada movimento desse tipo', 'ser segurada')).toBe(false);
    expect(matchesPortugueseOcrLine('', '')).toBe(false);
  });
});
