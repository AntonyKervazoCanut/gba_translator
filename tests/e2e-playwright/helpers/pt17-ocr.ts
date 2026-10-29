/** Normalise uniquement les variantes OCR de la sonde portugaise PT-17. */
export function normalizePortugueseOcr(text: string): string {
  // Vision peut émettre U+0430 pour le même bitmap que le a latin.
  return text.normalize('NFD').replace(/\p{M}/gu, '').replace(/\u0430/g, 'a')
    .replace(/\s+/g, ' ').trim();
}
