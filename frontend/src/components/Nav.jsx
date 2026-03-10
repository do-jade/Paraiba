export default function Nav({ onHome }) {
  return (
    <nav className="nav">
      <div className="nav-logo" onClick={onHome}>
        <span className="nav-logo-text">Paraíba</span>
      </div>
    </nav>
  )
}
