import { useEffect, useState } from 'react'
import axios from 'axios'
import css from './styles/styles'
import Nav from './components/Nav'
import HomePage from './pages/HomePage'
import CategoryPage from './pages/CategoryPage'
import LoadingPage from './pages/LoadingPage'
import ResultsPage from './pages/ResultsPage'
import DetailPage from './pages/DetailPage'

const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const normalizePlaces = (payload) => (Array.isArray(payload) ? payload : [])

export default function App() {
  const [places, setPlaces] = useState([])
  const [screen, setScreen] = useState('home')
  const [category, setCategory] = useState(null)
  const [label, setLabel] = useState('')
  const [loadStep, setLoadStep] = useState(0)
  const [place, setPlace] = useState(null)

  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
  }, [screen])

  const goHome = () => { setScreen('home'); setLoadStep(0) }

  const handleCategory = async (cat, lbl) => {
    setCategory(cat); setLabel(lbl); setLoadStep(0)
    setScreen('loading')
    ;[0, 1, 2, 3].forEach(i => {
      setTimeout(() => setLoadStep(i + 1), 500 + i * 500)
    })

    try {
      const keyword = cat === 'restaurants' ? 'Restaurant'
                    : cat === 'cafes' ? 'Cafe'
                    : 'Attraction'
      const res = await axios.get(`${API_BASE_URL}/api/paraiba?category=${keyword}&limit=50`)
      const nextPlaces = normalizePlaces(res.data)
      if (!Array.isArray(res.data)) {
        console.error('Expected array response for places, received:', res.data)
      }
      setPlaces(nextPlaces)
    } catch (err) {
      console.error('Failed to fetch places:', err)
      setPlaces([])
    }

    setTimeout(() => setScreen('results'), 2600)
  }

  // Called by ResultsPage when user changes filters
  const handleRefilter = async (cat, filters) => {
    try {
      const keyword = cat === 'restaurants' ? 'Restaurant'
                    : cat === 'cafes' ? 'Cafe'
                    : 'Attraction'
      const params = new URLSearchParams({ category: keyword, limit: 50 })
      if (filters.length > 0) params.append('categoryType', filters.join(','))
      const res = await axios.get(`${API_BASE_URL}/api/paraiba?${params.toString()}`)
      const nextPlaces = normalizePlaces(res.data)
      if (!Array.isArray(res.data)) {
        console.error('Expected array response for places, received:', res.data)
      }
      setPlaces(nextPlaces)
    } catch (err) {
      console.error('Failed to fetch places:', err)
      setPlaces([])
    }
  }

  return (
    <>
      <style>{css}</style>
      <Nav onHome={goHome} />
      <div className="page" key={screen}>
        {screen === 'home'     && <HomePage onExplore={() => setScreen('category')} />}
        {screen === 'category' && <CategoryPage onSelect={handleCategory} onBack={goHome} />}
        {screen === 'loading'  && <LoadingPage label={label} step={loadStep} />}
        {screen === 'results'  && <ResultsPage places={places} category={category} label={label} onSelect={(p) => { setPlace(p); setScreen('detail') }} onBack={() => setScreen('category')} onRefilter={handleRefilter} />}
        {screen === 'detail'   && <DetailPage place={place} label={label} onBack={() => setScreen('results')} />}
      </div>
    </>
  )
}
