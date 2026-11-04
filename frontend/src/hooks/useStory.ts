
import { useEffect, useState } from "react";
import type { Story } from "../types/story";

export function useStoryID(storyId: number | undefined | null) {
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!storyId || Number.isNaN(storyId)) {
      // nothing to load
      setStory(null);
      setLoading(false);
      setError(null);
      return;
    }

    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`/api/stories/${storyId}/`, {
          signal: controller.signal,
        });
        if (!res.ok) throw new Error("Failed to load <Story-Detail>");

        const json: Story = await res.json();
        setStory(json);
      } catch (err: any) {
        if (err?.name !== "AbortError") setError(err);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, [storyId]);

  return { story, loading, error };
}

export function useStorySlug(slug: string | undefined | null) {
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!slug) {
      // nothing to load
      setStory(null);
      setLoading(false);
      setError(null);
      return;
    }

    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`/api/stories/slug/${slug}/`, {
          signal: controller.signal,
        });
        if (!res.ok) throw new Error("Failed to load <Story-Detail>");

        const json: Story = await res.json();
        setStory(json);
      } catch (err: any) {
        if (err?.name !== "AbortError") setError(err);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, [slug]);

  return { story, loading, error };
}