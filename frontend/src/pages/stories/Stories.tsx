import { StoryCard } from '../../components/StoryCard'
import { useStories } from '../../hooks/useStories'
import StoryList from '../../components/StoryList'

export default function Stories() {
  const { stories, loading, error } = useStories(2)

  return (
    <main>
      <h1>Stories</h1>
      <StoryList/>
    </main>
  )
}
