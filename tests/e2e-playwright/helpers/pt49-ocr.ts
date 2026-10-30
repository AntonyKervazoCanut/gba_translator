/** Compare une ligne complète, avec une seule confusion de glyphe OCR permise. */
export function matchesPortugueseOcrLine(actual: string, expected: string): boolean {
  const normalize = (value: string) => value.normalize('NFD').replace(/\p{M}/gu, '')
    .replace(/\s+/g, ' ').trim().toLowerCase();
  const observed = normalize(actual);
  const reference = normalize(expected);
  return reference.length > 0 && observed.length === reference.length
    && [...reference].filter((char, i) => char !== observed[i]).length <= 1;
}
