// src/pages/StoryDetail.tsx
import { useLocation, useParams } from 'react-router-dom';
import type { Story } from '../../types/story';
import { useStorySlug } from '../../hooks/useStory';
import { useChapters } from '../../hooks/useChapters';

import ChapterCard from '../../components/ChapterCard'

type LocationState = { story?: Story };

export default function StoryDetail() {
  const { slug } = useParams<{ slug?: string }>();

  const location = useLocation();
  const state = location.state as LocationState | null;
  const storyFromState = state?.story;

  const { story: storyFromApi, loading:sLoading, error:sError } = useStorySlug(slug);
  const story = storyFromState ?? storyFromApi ?? undefined;
  const { chapters, loading:cLoading, error:cError } = useChapters(story?.id);
  if (!storyFromState && sLoading) return <div>Loading…</div>;
  if (sError && !story) return <div>Failed to load story.</div>;
  if (!story) return <div>Story not found.</div>;

  return (
    <main className="container">
      <h1>{story.title}</h1>
      <p style={{ color: "var(--color-muted)" }}>
        {story.author} • {story.last_updated}
      </p>
      <section className="story__list">
        {cLoading && (
          <div>Loading chapters...</div>
        )}

        {cError && (
          <div>
            Failed to load chapters: {cError.message}
          </div>
        )}

        {!cLoading && !cError && (!chapters || chapters.length === 0) && (
          <div>No chapters found.</div>
        )}

        {!cLoading && !cError && chapters && (
          <div className="story__list__items">
            {chapters.map((c) => (
              <ChapterCard chapter={c} slug={slug} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}