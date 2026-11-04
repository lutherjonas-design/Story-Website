import { StoryCard } from '../components/StoryCard'
import { useStories } from '../hooks/useStories'
 import './StoryList.css'

type StoryListProps = {
  /** If omitted, no limit is applied */
  limit?: number;
};


export default function StoryList({ limit }: StoryListProps) {
    const { stories, loading, error } = limit ? useStories(limit) : useStories()
    return (
        <section className="story__list">
            {loading && (
                <div>Loading stories…</div>
            )}

            {error && (
                <div>
                    Failed to load stories: {error.message}
                </div>
            )}

            {!loading && !error && (!stories || stories.length === 0) && (
                <div>No stories found.</div>
            )}

            {!loading && !error && stories && (
                <div className="story__list__items">
                    {stories.map((s) => (
                        <StoryCard key={String(s.id ?? s.title)} story={s} />
                    ))}
                </div>
            )}
        </section>
    )
}