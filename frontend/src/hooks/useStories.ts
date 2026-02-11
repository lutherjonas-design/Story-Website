
import { useEffect, useMemo, useState } from 'react'
import type { Story } from '../components/StoryCard'

type StoriesResponse =
  | Story[]
  | { results: Story[] }
  | { data: Story[] }
  | any // fallback if the shape varies

export function useStories(limit = 2) {
  const [data, setData] = useState<Story[] | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch('api/stories/', { signal: controller.signal })
        if (!res.ok) {
          throw new Error(`Failed to load stories (${res.status})`)
        }
        const json: StoriesResponse = await res.json()

        let stories: Story[] = []
        if (Array.isArray(json)) {
          stories = json
        } else if (json?.results && Array.isArray(json.results)) {
          stories = json.results
        } else if (json?.data && Array.isArray(json.data)) {
          stories = json.data
        } else {
          // last resort: try to coerce
          stories = []
        }

        setData(stories)
      } catch (e: any) {
        if (e.name !== 'AbortError') {
          setError(e)
        }
      } finally {
        setLoading(false)
      }
    }

    load()
    return () => controller.abort()
  }, [])

  const limited = useMemo(() => {
    if (!data) return null
    return data.slice(0, limit)
  }, [data, limit])

  return { stories: limited, allStories: data, loading, error }
}
