import { useState } from 'react'
import axios from 'axios'
import css from './styles/styles'
import Nav from './components/Nav'
import HomePage from './pages/HomePage'
import CategoryPage from './pages/CategoryPage'
import LoadingPage from './pages/LoadingPage'
import ResultsPage from './pages/ResultsPage'
import DetailPage from './pages/DetailPage'

export default function App() {
  // Basic app state for page flow + selected results.
  const [places, setPlaces] = useState([])
  const [screen, setScreen] = useState('home')
  const [category, setCategory] = useState(null)
  const [label, setLabel] = useState('')
  const [loadStep, setLoadStep] = useState(0)
  const [place, setPlace] = useState(null)

  // When user goes home, reset loading progress too.
  const goHome = () => { setScreen('home'); setLoadStep(0) }

  const handleCategory = async (cat, lbl) => {
    setCategory(cat); setLabel(lbl); setLoadStep(0)
    setScreen('loading')
    // Fake progress steps so loading screen feels alive.
    ;[0, 1, 2, 3].forEach(i => {
      setTimeout(() => setLoadStep(i + 1), 500 + i * 500)
    })

    try {
      // Backend expects singular words here.
      const keyword = cat === 'restaurants' ? 'Restaurant'
                    : cat === 'cafes' ? 'Cafe'
                    : 'Attraction'
      const res = await axios.get(`/api/paraiba?category=${keyword}`)
      console.log("API response:", res.data)
      console.log("First place:", res.data[0])
      console.log("First place comments:", res.data[0]?.comments)
      setPlaces(res.data)
    } catch (err) {
      console.error('Failed to fetch places:', err)
      setPlaces([])
    }

    // Small delay so users can actually see the loading steps finish.
    setTimeout(() => setScreen('results'), 2600)
  }

  return (
    <>
      <style>{css}</style>
      <Nav onHome={goHome} />
      <div className="page" key={screen}>
        {screen === 'home'     && <HomePage onExplore={() => setScreen('category')} />}
        {screen === 'category' && <CategoryPage onSelect={handleCategory} onBack={goHome} />}
        {screen === 'loading'  && <LoadingPage label={label} step={loadStep} />}
        {screen === 'results'  && <ResultsPage places={places} category={category} label={label} onSelect={(p) => { setPlace(p); setScreen('detail') }} onBack={() => setScreen('category')} />}
        {screen === 'detail'   && <DetailPage place={place} label={label} onBack={() => setScreen('results')} />}
      </div>
    </>
  )
}
