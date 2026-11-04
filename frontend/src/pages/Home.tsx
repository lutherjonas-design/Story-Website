import './Home.css'
import StoryList from '../components/StoryList'

export default function Home() {
  return (
    <main>
      <section>
        <h1>Welcome</h1>
        <p>
          Here are a couple of stories fetched from <code>/api/stories/</code>.
        </p>
      </section>
      < StoryList limit={2} />

    </main>
  )
}
