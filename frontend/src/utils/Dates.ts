
export function parseDateSafe(input: string): Date | null {
  if (!input) return null;

  // Case A: ISO (e.g., "2026-02-04T22:57:06Z" or "2026-02-04")
  // Fast-path: if it matches an ISO-like pattern, trust the native parser
  if (/^\d{4}-\d{2}-\d{2}/.test(input)) {
    const d = new Date(input);
    return isNaN(d.getTime()) ? null : d;
  }

  // Case B: DD.MM.YYYY or DD.MM.YYYY HH:mm
  const match = input.match(
    /^(\d{1,2})\.(\d{1,2})\.(\d{4})(?:[ T](\d{1,2}):(\d{2}))?$/
  );
  if (match) {
    const [, ddStr, mmStr, yyyyStr, hhStr, minStr] = match;
    const dd = Number(ddStr);
    const mm = Number(mmStr);     // 1–12
    const yyyy = Number(yyyyStr);
    const hh = hhStr ? Number(hhStr) : 0;
    const min = minStr ? Number(minStr) : 0;

    // Create in local time; month is 0-based in JS Date
    const d = new Date(yyyy, mm - 1, dd, hh, min, 0, 0);

    // Validate in case of overflow (e.g., 31.02.2026)
    if (
      d.getFullYear() === yyyy &&
      d.getMonth() === mm - 1 &&
      d.getDate() === dd &&
      d.getHours() === hh &&
      d.getMinutes() === min
    ) {
      return d;
    }
    return null; // invalid combination
  }

  // Fallback: try native parse (not recommended, but last resort)
  const tentative = new Date(input);
  return isNaN(tentative.getTime()) ? null : tentative;
}


export function timeAgo(input: string): string {
  const date = parseDateSafe(input);
  if (!date) return ""; // or "unknown"

  const now = new Date();

  let diffSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  // Treat future values (e.g., server UTC vs local) as "just now"
  if (diffSeconds < 0) diffSeconds = 0;

  if (diffSeconds < 60) return "just now";

  const minutes = Math.floor(diffSeconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? "" : "s"} ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`;

  const days = Math.floor(hours / 24);
  if (days < 30) return `${days} day${days === 1 ? "" : "s"} ago`;

  const months = Math.floor(days / 30); // approximate is fine for "time ago"
  if (months < 12) return `${months} month${months === 1 ? "" : "s"} ago`;

  const years = Math.floor(days / 365);
  return `${years} year${years === 1 ? "" : "s"} ago`;
}
