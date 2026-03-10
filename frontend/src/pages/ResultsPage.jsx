import BackBtn from '../components/BackBtn'

export default function ResultsPage({ places, category, label, onSelect, onBack }) {
  if (places.length === 0) {
    return (
      <div className="error-state">
        <span className="error-icon">🔍</span>
        <p className="error-title">No results found</p>
        <p className="error-sub">Try a different category</p>
        <button className="error-btn" onClick={onBack}>Go Back</button>
      </div>
    )
  }

  return (
    <>
      <BackBtn onClick={onBack} />
      <div className="results-header fu">
        <p className="results-eyebrow">Ranked by sentiment + local engagement</p>
        <h2 className="results-title">Top <span>{label}</span> in GNV</h2>
      </div>
      {places.map((p, i) => (
        <div
          key={p._id}
          className={`result-card fu${Math.min(i + 1, 5)}${i === 0 ? ' top' : ''}`}
          onClick={() => onSelect(p)}
        >
          <div className="result-top-row">
            <span className="result-num">#{p.ranking}</span>
            <span className="result-badge">Hidden Gem</span>
          </div>
          <p className="result-name">{p.name}</p>
          <p className="result-desc">{p.description}</p>
          <span className="result-cta">View details →</span>
        </div>
      ))}
    </>
  )
}
