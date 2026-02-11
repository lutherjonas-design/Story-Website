import StoryCard from '../components/StoryCard'
import { useStories } from '../hooks/useStories'

export default function Home() {
  const { stories, loading, error } = useStories(2)

  return (
    <main className="mx-auto max-w-6xl px-4 py-6">
      <section className="mb-6">
        <h1 className="text-2xl font-bold">Welcome</h1>
        <p className="mt-1 text-gray-600">
          Here are a couple of stories fetched from <code>/api/stories/</code>.
        </p>
      </section>

      {loading && (
        <div className="text-gray-600">Loading stories…</div>
      )}

      {error && (
        <div className="rounded-md border border-red-200 bg-red-50 p-3 text-red-700">
          Failed to load stories: {error.message}
        </div>
      )}

      {!loading && !error && (!stories || stories.length === 0) && (
        <div className="text-gray-600">No stories found.</div>
      )}

      {!loading && !error && stories && (
        <div className="grid gap-4 sm:grid-cols-2">
          {stories.map((s) => (
            <StoryCard key={String(s.id ?? s.title)} story={s} />
          ))}
        </div>
      )}
    </main>
  )
}
