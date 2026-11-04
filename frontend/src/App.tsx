
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Stories from './pages/stories/Stories'
import NotFound from './pages/NotFound'
import StoryDetail from './pages/stories/storyDetail'
import ChapterRead from './pages/stories/ChapterRead'
import Transfer from './pages/dict/Dictionary'


export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        {/*Static Routes*/}
        <Route path="/" element={ <Home/> }/>
        <Route path="/stories" element={ <Stories/> }/>
        <Route path="/dictionary" element={ <Transfer /> }/>
        <Route path="/transfer" element={ <Transfer/> }/>
        {/*Dynamic Routes*/}
        <Route path="/s/:slug" element={<StoryDetail/> }/>
        <Route path="/s/:slug/:id" element={<ChapterRead/> }/>
        {/*Fallback Route*/}
        <Route path="*" element={ <NotFound /> }/>
      </Routes>
    </BrowserRouter>
  )
}
