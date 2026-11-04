import { useEffect, useState } from "react";
import { Chapter } from "../types/chapter"

export function useChapters(storyId?: number) {
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!storyId) {
      setLoading(false);
      setError(null);
      return;
    }

    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        const res = await fetch(`/api/stories/${storyId}/chapters/`, {
          signal: controller.signal,
        });
        if (!res.ok) throw new Error("Failed to load chapters");

        const json = await res.json();
        setChapters(json);
      } catch (err: any) {
        if (err.name !== "AbortError") setError(err);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, [storyId]);

  return { chapters, loading, error };
}
