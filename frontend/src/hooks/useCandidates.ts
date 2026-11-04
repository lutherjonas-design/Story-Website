import { useEffect, useState } from "react";
import { Word } from "../types/word";

type Props = {
  limit?: number
  prefix?: string
}

export function useCandidates({ limit, prefix }: Props) {
  const [words, setWords] = useState<Word[] | []>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [reloadIndex, setReloadIndex] = useState(0);

  const reload = () => setReloadIndex((i) => i + 1);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const params = [];
        if (prefix) params.push(`prefix=${prefix}`);
        if (limit) params.push(`limit=${limit}`);
        const query = params.length ? `?${params.join("&")}` : "";

        const res = await fetch(`/api/dict/candidates/${query}`, {
          signal: controller.signal,
        });
        if (!res.ok) {
          throw new Error(`Failed to load candidates (${res.status})`);
        }

        const json: Word[] = await res.json();
        setWords(json);
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, [prefix, limit, reloadIndex]);
  // dependencies: refresh when prefix/limit changes OR reload()

  return { words, loading, error, reload };
}