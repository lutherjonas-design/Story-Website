// src/utils/slug.ts
export function slugify(input: string): string {
  return input
    .toLowerCase()
    .normalize("NFKD")               // split accents
    .replace(/[\u0300-\u036f]/g, "") // remove diacritics
    .replace(/[^a-z0-9]+/g, "-")     // non-alphanumeric -> dashes
    .replace(/^-+|-+$/g, "")         // trim
    .slice(0, 80);                   // safety cutoff
}