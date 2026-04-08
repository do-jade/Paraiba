import { useState } from 'react'
import BackBtn from '../components/BackBtn'

const RESTAURANT_GROUPS = [
  {
    group: 'Cuisine',
    cats: [
      { key: 'american',      label: 'American',      icon: '🍔' },
      { key: 'italian',       label: 'Italian',       icon: '🍝' },
      { key: 'mexican',       label: 'Mexican',       icon: '🌮' },
      { key: 'japanese',      label: 'Japanese',      icon: '🍣' },
      { key: 'chinese',       label: 'Chinese',       icon: '🥢' },
      { key: 'mediterranean', label: 'Mediterranean', icon: '🫒' },
      { key: 'thai',          label: 'Thai',          icon: '🥜' },
      { key: 'indian',        label: 'Indian',        icon: '🍛' },
      { key: 'korean',        label: 'Korean',        icon: '🥘' },
      { key: 'vietnamese',    label: 'Vietnamese',    icon: '🍜' },
      { key: 'bbq',           label: 'BBQ',           icon: '🔥' },
      { key: 'seafood',       label: 'Seafood',       icon: '🦞' },
      { key: 'burgers',       label: 'Burgers',       icon: '🍔' },
      { key: 'sandwiches',    label: 'Sandwiches',    icon: '🥪' },
      { key: 'caribbean',     label: 'Caribbean',     icon: '🌴' },
      { key: 'steakhouse',    label: 'Steakhouse',    icon: '🥩' },
    ],
  },
  {
    group: 'Cafe & Drinks',
    cats: [
      { key: 'cafe',     label: 'Cafe',     icon: '☕' },
      { key: 'bakery',   label: 'Bakery',   icon: '🥐' },
      { key: 'dessert',  label: 'Dessert',  icon: '🍨' },
      { key: 'bar',      label: 'Bar',      icon: '🍸' },
      { key: 'brewery',  label: 'Brewery',  icon: '🍺' },
      { key: 'winery',   label: 'Winery',   icon: '🍷' },
    ],
  },
  {
    group: 'Dining Options',
    cats: [
      { key: 'indoor',         label: 'Indoor',           icon: '🏠' },
      { key: 'outdoor',        label: 'Outdoor',          icon: '🌿' },
    ],
  },
  
]

const ATTRACTION_GROUPS = [
  {
    group: 'Outdoors & Nature',
    cats: [
      { key: 'hiking',      label: 'Hiking',         icon: '🥾' },
      { key: 'park',        label: 'Parks',          icon: '🌳' },
      { key: 'water sports',label: 'Water Sports',   icon: '🛶' },
      { key: 'swimming',    label: 'Swimming',       icon: '🏊' },
      { key: 'cycling',     label: 'Cycling',        icon: '🚴' },
      { key: 'camping',     label: 'Camping',        icon: '⛺' },
      { key: 'wildlife',    label: 'Wildlife',       icon: '🦅' },
      { key: 'water body',  label: 'Lakes & Rivers', icon: '💧' },
    ],
  },
  {
    group: 'Arts & Entertainment',
    cats: [
      { key: 'museum',          label: 'Museum',        icon: '🏛️' },
      { key: 'performing arts', label: 'Arts & Theater',icon: '🎭' },
      { key: 'arcade',          label: 'Arcade & Fun',  icon: '🎮' },
      { key: 'fitness',         label: 'Fitness',       icon: '🏋️' },
      { key: 'market',          label: 'Markets',       icon: '🛍️' },
    ],
  },
  {
    group: 'Setting',
    cats: [
      { key: 'indoor',         label: 'Indoor',           icon: '🏠' },
      { key: 'outdoor',        label: 'Outdoor',          icon: '🌿' },
      { key: 'indoor/outdoor', label: 'Indoor & Outdoor', icon: '⛅' },
    ],
  },
  
]

const PAGE_SIZE = 10

export default function ResultsPage({ places, category, label, onSelect, onBack, onRefilter }) {
  const [selectedTypes, setSelectedTypes] = useState([])
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const safePlaces = Array.isArray(places) ? places : []

  const groups = category === 'restaurants' ? RESTAURANT_GROUPS : ATTRACTION_GROUPS

  const applyFilters = (newTypes) => {
    setVisibleCount(PAGE_SIZE)
    onRefilter(category, newTypes)
  }

  const handleToggle = (key) => {
    const next = selectedTypes.includes(key)
      ? selectedTypes.filter(k => k !== key)
      : [...selectedTypes, key]
    setSelectedTypes(next)
    applyFilters(next)
  }

  const clearAll = () => {
    setSelectedTypes([])
    applyFilters([])
  }

  const visiblePlaces = safePlaces.slice(0, visibleCount)
  const hasMore = visibleCount < safePlaces.length

  const getPrimaryType = (place) => {
    const rawTypes = Array.isArray(place.categoryType)
      ? place.categoryType
      : typeof place.categoryType === 'string'
      ? place.categoryType.split(',')
      : []

    const cleanedTypes = rawTypes
      .map(type => String(type).trim())
      .filter(Boolean)
      .filter(type => !['indoor', 'outdoor', 'indoor/outdoor', 'general'].includes(type.toLowerCase()))

    if (cleanedTypes.length === 0) return null

    const primary = cleanedTypes[0]
    return primary
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const getDisplayTypes = (place) => {
    const rawTypes = Array.isArray(place.categoryType)
      ? place.categoryType
      : typeof place.categoryType === 'string'
      ? place.categoryType.split(',')
      : []

    return rawTypes
      .map(type => String(type).trim())
      .filter(Boolean)
      .filter(type => type.toLowerCase() !== 'general')
      .slice(0, 3)
      .map(type =>
        type
          .split(' ')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ')
      )
  }

  const sidebar = (
    <aside className="results-sidebar">
      {/* Grouped category filters */}
      <div className="sidebar-section">
        <div className="sidebar-section-header">
          <p className="sidebar-section-label">Filter by type</p>
          {selectedTypes.length > 0 && (
            <button className="sidebar-clear-btn" onClick={clearAll}>Clear all</button>
          )}
        </div>

        {groups.map(g => (
          <div key={g.group} className="sidebar-group-card">
            <p className="sidebar-group-title">{g.group}</p>
            <div className={`sidebar-filter-list${g.group === 'Dining Options' ? ' checkbox-list' : ''}`}>
              {g.cats.map(c => (
                <button
                  key={c.key}
                  className={`sidebar-filter-item${selectedTypes.includes(c.key) ? ' active' : ''}${g.group === 'Dining Options' ? ' checkbox-item' : ''}`}
                  onClick={() => handleToggle(c.key)}
                >
                  <span className="sidebar-filter-pill">
                    {g.group === 'Dining Options' && (
                      <span className={`sidebar-checkbox-box${selectedTypes.includes(c.key) ? ' active' : ''}`}>
                        {selectedTypes.includes(c.key) ? '✓' : ''}
                      </span>
                    )}
                    <span className="sidebar-filter-label">{c.label}</span>
                    {g.group !== 'Dining Options' && selectedTypes.includes(c.key) && <span className="sidebar-filter-check">✓</span>}
                  </span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </aside>
  )

  return (
    <>
      <BackBtn onClick={onBack} />
      <div className="results-header fu">
        <p className="results-eyebrow">Ranked by sentiment + local engagement</p>
        <h2 className="results-title">Top <span>{label}</span> in GNV</h2>
        {selectedTypes.length > 0 && (
          <p className="results-filter-hint">{selectedTypes.length} filter{selectedTypes.length > 1 ? 's' : ''} active</p>
        )}
      </div>

      {/* Mobile filter toggle */}
      <button className="mobile-filter-btn" onClick={() => setSidebarOpen(o => !o)}>
        {sidebarOpen ? 'Hide Filters' : `Filters${selectedTypes.length > 0 ? ' (' + selectedTypes.length + ')' : ''}`}
      </button>
      {sidebarOpen && <div className="mobile-sidebar-drawer">{sidebar}</div>}

      {/* Two-column layout */}
      <div className="results-layout">
        <div className="results-sidebar-wrap">{sidebar}</div>

        <div className="results-main">
          {safePlaces.length === 0 ? (
            <div className="error-state" style={{ marginTop: '40px' }}>
              <span className="error-icon">🔍</span>
              <p className="error-title">No results found</p>
              <p className="error-sub">Try adjusting your filters</p>
              <button className="error-btn" onClick={clearAll}>Clear Filters</button>
            </div>
          ) : (
            visiblePlaces.map((p, i) => (
              <div
                key={p._id}
                className={`result-card fu${Math.min(i + 1, 5)}${i === 0 ? ' top' : ''}`}
                onClick={() => onSelect(p)}
              >
                <div className="result-header-row">
                  <p className="result-name">{p.name}</p>
                  <p className="result-score-line">Gem Score {p.ranking}</p>
                </div>
                <p className="result-desc" style={{
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {p.description
                    ? p.description
                    : p.comments && p.comments.length > 0
                    ? `"${p.comments[0].text}"`
                    : null}
                </p>
                <div className="result-meta-row bottom">
                  {getDisplayTypes(p).length > 0 ? (
                    getDisplayTypes(p).map(type => (
                      <span key={type} className="result-chip subtle">{type}</span>
                    ))
                  ) : getPrimaryType(p) ? (
                    <span className="result-meta-text">{getPrimaryType(p)}</span>
                  ) : null}
                </div>
                <span className="result-cta">View details →</span>
              </div>
            ))
          )}
          {hasMore && (
            <button
              className="load-more-btn"
              onClick={() => setVisibleCount(c => c + PAGE_SIZE)}
            >
              Show more results
              <span className="load-more-count">
                {safePlaces.length - visibleCount} remaining
              </span>
            </button>
          )}
        </div>
      </div>
    </>
  )
}