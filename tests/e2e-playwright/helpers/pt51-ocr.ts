/** Vérifie chaque ligne entière dans une lecture du même écran, sans réparer les mots. */
export function hasPortugueseOcrLines(readings: string[], lines: string[]): boolean {
  const normalize = (text: string): string => text.normalize('NFD')
    .replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim().toLowerCase();
  return lines.length > 0 && lines.every(line =>
    normalize(line).length > 0 && readings.some(text => normalize(text).includes(normalize(line))));
}
