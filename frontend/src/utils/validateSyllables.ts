export function validateSyllables(word: string, syllables: string[]): boolean {
  const full = syllables.join("").toLowerCase().trim();
  const target = word.toLowerCase().trim();
  return full === target;
}