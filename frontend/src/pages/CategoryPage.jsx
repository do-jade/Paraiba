import BackBtn from '../components/BackBtn'

const ICONS = { restaurants: '🍴', attractions: '🌿' }

export default function CategoryPage({ onSelect, onBack }) {
  const cats = [
    // Restaurants, cafes, and attractions
    { key: 'restaurants', label: 'Restaurants' },
    { key: 'attractions', label: 'Attractions' },
  ]
  return (
    <>
      <BackBtn onClick={onBack} />
      <div className="cat-header fu">
        <p className="cat-eyebrow">Step 1 of 1</p>
        <h2 className="cat-title">What are you exploring?</h2>
      </div>
      <div className="cat-grid">
        {cats.map((c, i) => (
          <div key={c.key} className={`cat-card fu${i + 1}`} onClick={() => onSelect(c.key, c.label)}>
            <div className="cat-icon-wrap">{ICONS[c.key]}</div>
            <span className="cat-label">{c.label}</span>
          </div>
        ))}
      </div>
    </>
  )
}
