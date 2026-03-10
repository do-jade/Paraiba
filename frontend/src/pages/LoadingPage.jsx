export default function LoadingPage({ label, step }) {
  const steps = [
    { label: 'Scraping r/GNV posts', done: step > 0, active: step === 0 },
    { label: `Extracting ${label} mentions`, done: step > 1, active: step === 1 },
    { label: 'Running sentiment analysis', done: step > 2, active: step === 2 },
    { label: 'Ranking results', done: step > 3, active: step === 3 },
  ]
  return (
    <div className="loading">
      <div className="loading-visual">
        <div className="loading-ring" />
        <div className="loading-ring-inner" />
        <div className="loading-gem-sm">💎</div>
      </div>
      <p className="loading-title">Analyzing discussions</p>
      <p className="loading-sub">Finding hidden gems for {label}</p>
      <div className="loading-steps">
        {steps.map((s, i) => (
          <div key={i} className={`loading-step${s.active ? ' active' : ''}${s.done ? ' done' : ''}`}>
            <div className="step-dot" />
            {s.done ? '✓ ' : ''}{s.label}
          </div>
        ))}
      </div>
    </div>
  )
}
