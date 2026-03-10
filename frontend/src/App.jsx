import { useState } from "react"
import axios from "axios"

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Jost:wght@300;400;500;600;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html, body, #root { width: 100%; height: 100%; }
  body { background: #f7f6f2; font-family: 'Jost', sans-serif; color: #1a1a2e; -webkit-font-smoothing: antialiased; }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }

  .fu  { animation: fadeUp 0.5s cubic-bezier(0.22,1,0.36,1) both; }
  .fu1 { animation: fadeUp 0.5s 0.07s  cubic-bezier(0.22,1,0.36,1) both; }
  .fu2 { animation: fadeUp 0.5s 0.14s  cubic-bezier(0.22,1,0.36,1) both; }
  .fu3 { animation: fadeUp 0.5s 0.21s  cubic-bezier(0.22,1,0.36,1) both; }
  .fu4 { animation: fadeUp 0.5s 0.28s  cubic-bezier(0.22,1,0.36,1) both; }
  .fu5 { animation: fadeUp 0.5s 0.35s  cubic-bezier(0.22,1,0.36,1) both; }

  /* ── NAV ── */
  .nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    display: flex; justify-content: center; align-items: center;
    padding: 18px 40px;
    border-bottom: 1px solid rgba(26,26,46,0.07);
    background: rgba(247,246,242,0.9);
    backdrop-filter: blur(20px);
  }
  .nav-logo {
    display: flex; align-items: center; gap: 9px;
    cursor: pointer; user-select: none;
  }
  .nav-logo-text {
    font-family: 'Libre Baskerville', serif;
    font-size: 20px; font-weight: 700;
    letter-spacing: 0.01em; color: #1a1a2e;
    line-height: 1;
  }

  /* ── PAGE ── */
  .page {
    width: 100%; max-width: 860px;
    margin: 0 auto;
    padding: 100px 28px 80px;
    min-height: 100vh;
    display: flex; flex-direction: column; align-items: center;
  }

  /* ── BACK BTN ── */
  .back {
    display: flex; align-items: center; gap: 8px;
    background: none; border: none; cursor: pointer;
    font-family: 'Jost', sans-serif;
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #9ca3af;
    padding: 0; align-self: flex-start;
    transition: color 0.2s; margin-bottom: 40px;
  }
  .back:hover { color: #1a1a2e; }

  /* ── HOME ── */
  .home {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding-top: 20px; gap: 0;
  }
  .home-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 18px;
  }
  .home-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 5vw, 48px); font-weight: 900;
    line-height: 1.1; color: #1a1a2e; margin-bottom: 18px;
    white-space: nowrap;
  }
  .home-title em { font-style: italic; color: #2ec4b6; font-weight: 700; }
  .home-sub {
    font-size: 14px; color: #6b7280; line-height: 1.8;
    max-width: 360px; font-weight: 300; margin-bottom: 36px;
  }
  .home-btn {
    padding: 15px 48px; background: #1a1a2e; color: #f7f6f2;
    border: none; border-radius: 3px;
    font-family: 'Jost', sans-serif;
    font-size: 12px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
  }
  .home-btn:hover {
    background: #2ec4b6;
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(46,196,182,0.3);
  }
  .home-stats {
    display: flex; gap: 40px; margin-top: 52px;
    padding-top: 40px; border-top: 1px solid #e5e3dc;
  }
  .stat { text-align: center; }
  .stat-num {
    font-family: 'Jost', sans-serif;
    font-size: 22px; font-weight: 700; color: #1a1a2e;
    display: block; line-height: 1; letter-spacing: 0.04em;
  }
  .stat-label {
    font-size: 10px; font-weight: 500; letter-spacing: 0.12em;
    text-transform: uppercase; color: #9ca3af; margin-top: 4px;
    display: block;
  }
    /* ── CATEGORY ── */
  .cat-header { text-align: center; margin-bottom: 40px; width: 100%; }
  .cat-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 0.2em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 10px;
  }
  .cat-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 900; color: #1a1a2e;
  }
  .cat-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; width: 100%;
  }
  .cat-card {
    background: #fff; border-radius: 14px;
    padding: 32px 16px 26px;
    display: flex; flex-direction: column;
    align-items: center; gap: 14px;
    cursor: pointer; border: 1.5px solid #ece9e1;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
  }
  .cat-card::before {
    content: ''; position: absolute;
    inset: 0; background: linear-gradient(135deg, rgba(46,196,182,0.06), transparent);
    opacity: 0; transition: opacity 0.2s;
  }
  .cat-card:hover { transform: translateY(-5px); border-color: #2ec4b6; box-shadow: 0 16px 36px rgba(46,196,182,0.14); }
  .cat-card:hover::before { opacity: 1; }
  .cat-icon-wrap {
    width: 64px; height: 64px; border-radius: 50%;
    background: #f7f6f2; display: flex;
    align-items: center; justify-content: center;
    font-size: 26px; border: 1.5px solid #ece9e1;
    transition: border-color 0.2s, background 0.2s;
  }
  .cat-card:hover .cat-icon-wrap { border-color: #2ec4b6; background: rgba(46,196,182,0.06); }
  .cat-label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #1a1a2e;
  }
    /* ── LOADING ── */
  .loading {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 0;
    text-align: center;
  }
  .loading-visual {
    position: relative; width: 80px; height: 80px; margin-bottom: 36px;
  }
  .loading-ring {
    width: 80px; height: 80px; border-radius: 50%;
    border: 1.5px solid #ece9e1;
    border-top-color: #2ec4b6;
    animation: spin 1s linear infinite;
    position: absolute;
  }
  .loading-ring-inner {
    width: 56px; height: 56px; border-radius: 50%;
    border: 1.5px solid #ece9e1;
    border-bottom-color: rgba(46,196,182,0.4);
    animation: spin 1.6s linear infinite reverse;
    position: absolute; top: 12px; left: 12px;
  }
  .loading-gem-sm { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); font-size: 20px; }
  .loading-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px; font-weight: 900; color: #1a1a2e; margin-bottom: 10px;
  }
  .loading-sub {
    font-size: 12px; color: #9ca3af; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 36px;
    animation: pulse 1.8s ease infinite;
  }
  .loading-steps { display: flex; flex-direction: column; gap: 10px; width: 260px; }
  .loading-step {
    display: flex; align-items: center; gap: 12px;
    font-size: 12px; color: #9ca3af; font-weight: 400;
  }
  .loading-step.active { color: #1a1a2e; font-weight: 500; }
  .step-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #ece9e1; flex-shrink: 0;
    transition: background 0.3s;
  }
  .loading-step.active .step-dot { background: #2ec4b6; }
  .loading-step.done .step-dot { background: #2ec4b6; }
  .loading-step.done { color: #6b7280; }
  /* ── RESULTS ── */
  .results-header { width: 100%; text-align: center; margin-bottom: 28px; }
  .results-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 0.2em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 8px;
  }
  .results-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 900; color: #1a1a2e;
  }
  .result-card {
    width: 100%; background: #fff; border-radius: 14px;
    padding: 20px 22px; margin-bottom: 10px;
    display: flex; flex-direction: column; gap: 8px;
    cursor: pointer; border: 1.5px solid #ece9e1;
    transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
  }
  .result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
    border-color: #2ec4b6;
  }
  .result-card.top { border-color: #2ec4b6; }
  .result-top-row { display: flex; justify-content: space-between; align-items: center; }
  .result-num {
    font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #2ec4b6;
  }
  .results-title span { font-style: italic; color: #2ec4b6; }
  .result-badge {
    font-size: 9px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #2ec4b6;
    background: rgba(46,196,182,0.1);
    padding: 4px 10px; border-radius: 20px;
  }
  .result-name {
    font-size: 15px; font-weight: 600; color: #1a1a2e; line-height: 1.3;
  }
  .result-desc {
    font-size: 12px; color: #6b7280; line-height: 1.7; font-weight: 300;
  }
  .result-cta {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #2ec4b6; align-self: flex-end;
    margin-top: 4px;
  }
  .error-state {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; gap: 16px;
  }
  .error-icon { font-size: 40px; }
  .error-title { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900; color: #1a1a2e; }
  .error-sub { font-size: 13px; color: #6b7280; font-weight: 300; }
  .error-btn {
    margin-top: 8px; padding: 12px 32px;
    background: #1a1a2e; color: #f7f6f2; border: none;
    border-radius: 3px; font-family: 'Jost', sans-serif;
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; cursor: pointer;
  }

  /* ── DETAIL ── */
  .detail-breadcrumb {
    font-size: 11px; color: #9ca3af; letter-spacing: 0.05em;
    margin-bottom: 20px; align-self: flex-start;
  }
  .detail-card {
    width: 100%; background: #fff; border-radius: 16px;
    overflow: hidden; border: 1.5px solid #ece9e1; margin-bottom: 16px;
  }
  .detail-map {
    width: 100%; height: 200px;
    position: relative; overflow: hidden;
    background: #e4f4f3;
  }
  .map-placeholder {
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 10px; background: #f0faf9;
    border-bottom: 1.5px dashed #b2e4df;
  }
  .map-placeholder-icon { font-size: 28px; }
  .map-placeholder-text {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #9ca3af;
  }
  .map-placeholder-address {
    font-size: 12px; color: #2ec4b6; font-weight: 500;
  }
  .map-open-btn {
    position: absolute; bottom: 12px; right: 12px;
    background: #1a1a2e; color: #f7f6f2;
    font-family: 'Jost', sans-serif;
    font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; border: none; border-radius: 4px;
    padding: 7px 14px; cursor: pointer;
    transition: background 0.2s;
    text-decoration: none; display: flex; align-items: center; gap: 6px;
  }
  .map-open-btn:hover { background: #2ec4b6; }
  .detail-body { padding: 24px 26px; }
  .detail-cat {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 8px;
  }
  .detail-name {
    font-family: 'Playfair Display', serif;
    font-size: 26px; font-weight: 900; color: #1a1a2e;
    margin-bottom: 12px; line-height: 1.2;
  }
  .detail-desc {
    font-size: 13px; color: #6b7280; line-height: 1.8; font-weight: 300;
    margin-bottom: 18px;
  }
  .detail-meta {
    display: flex; justify-content: space-between; padding-top: 16px;
    border-top: 1px solid #f0ede6;
  }
  .meta-item { display: flex; flex-direction: column; align-items: center; gap: 2px; flex: 1; }
  .meta-label {
    font-size: 9px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #9ca3af;
  }
  .meta-value { font-size: 13px; font-weight: 600; color: #1a1a2e; }
  .comments-heading {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #9ca3af;
    margin-bottom: 12px; align-self: flex-start;
  }
  .comment-card {
    width: 100%; background: #fff; border-radius: 10px;
    padding: 15px 18px; margin-bottom: 8px;
    display: flex; justify-content: space-between;
    align-items: flex-start; gap: 16px;
    border: 1.5px solid #ece9e1;
    transition: border-color 0.2s;
  }
  .comment-card:hover { border-color: rgba(46,196,182,0.4); }
  .comment-body { display: flex; flex-direction: column; gap: 4px; flex: 1; }
  .comment-text { font-size: 13px; color: #374151; line-height: 1.65; font-weight: 300; }
  .comment-source { font-size: 10px; color: #9ca3af; font-weight: 500; letter-spacing: 0.04em; }
  .comment-upvotes {
    font-size: 11px; font-weight: 700; color: #2ec4b6;
    white-space: nowrap; background: rgba(46,196,182,0.08);
    padding: 4px 10px; border-radius: 20px; flex-shrink: 0;
    margin-top: 2px;
  }

  /* ── RESPONSIVE ── */
  @media (max-width: 520px) {
    .page { padding: 90px 18px 60px; }
    .home-stats { gap: 24px; }
    .cat-grid { grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .cat-card { padding: 24px 10px 20px; }
    .cat-icon-wrap { width: 50px; height: 50px; font-size: 20px; }
    .home-title { font-size: 28px; }
  }
`
/* Last update 030926
const PLACES = {
  restaurants: [
    { id: 1, name: "Satch's Pizza", address: "1800 W University Ave, Gainesville, FL", desc: "A Gainesville staple loved by locals for decades. Incredible brick-oven slices tucked away from tourist trails.", sentiment: "94% positive", mentions: "142 mentions" },
    { id: 2, name: "Leonardo's By the Slice", address: "1245 W University Ave, Gainesville, FL", desc: "Old-school pizza joint near campus, consistently praised for its authentic flavors and unassuming vibe.", sentiment: "89% positive", mentions: "98 mentions" },
    { id: 3, name: "Emiliano's Cafe", address: "7 SE 1st Ave, Gainesville, FL", desc: "Latin-inspired dishes made with local ingredients. A hidden gem that regulars fiercely protect.", sentiment: "87% positive", mentions: "76 mentions" },
    { id: 4, name: "Dragonfly Sushi", address: "201 SE 2nd Ave, Gainesville, FL", desc: "Creative sushi in a cozy setting. Locals rave about the omakase options unavailable on main menus.", sentiment: "85% positive", mentions: "61 mentions" },
    { id: 5, name: "Ward's Supermarket Deli", address: "516 NW 23rd Ave, Gainesville, FL", desc: "Old Florida charm with a legendary deli counter. More of an experience than just a meal.", sentiment: "82% positive", mentions: "54 mentions" },
  ],
  cafes: [
    { id: 1, name: "Volta Coffee", address: "1300 NW 17th Ave, Gainesville, FL", desc: "Third-wave coffee done right. A local favorite for serious coffee drinkers and remote workers alike.", sentiment: "96% positive", mentions: "188 mentions" },
    { id: 2, name: "Maude's Classic Cafe", address: "101 SE 2nd Pl, Gainesville, FL", desc: "Bohemian vibes, excellent espresso, and a loyal local crowd. The anti-Starbucks of Gainesville.", sentiment: "91% positive", mentions: "134 mentions" },
    { id: 3, name: "Karma Cream", address: "621 W University Ave, Gainesville, FL", desc: "Organic soft-serve and coffee in a laid-back setting. Adored by the local community for years.", sentiment: "88% positive", mentions: "89 mentions" },
    { id: 4, name: "Pascal's Coffeehouse", address: "1132 W University Ave, Gainesville, FL", desc: "Quiet, unpretentious spot near campus. Perfect for long study sessions with great pour-overs.", sentiment: "86% positive", mentions: "72 mentions" },
    { id: 5, name: "Sweetwater Coffee Bar", address: "300 SW 4th Ave, Gainesville, FL", desc: "Intimate neighborhood cafe with rotating single-origin beans and homemade pastries.", sentiment: "83% positive", mentions: "58 mentions" },
  ],
  parks: [
    { id: 1, name: "Sweetwater Wetlands", address: "3510 NW 34th St, Gainesville, FL", desc: "A stunning urban wetlands that locals treat as their secret nature escape. Incredible birdwatching.", sentiment: "97% positive", mentions: "210 mentions" },
    { id: 2, name: "Paynes Prairie Preserve", address: "100 Savannah Blvd, Micanopy, FL", desc: "Wild Florida at its finest — bison, wild horses, and endless trails hidden in plain sight.", sentiment: "95% positive", mentions: "176 mentions" },
    { id: 3, name: "Depot Park", address: "200 SE Depot Ave, Gainesville, FL", desc: "Renovated historic rail yard turned community park. A beloved local gathering spot with great trails.", sentiment: "90% positive", mentions: "121 mentions" },
    { id: 4, name: "Boulware Springs Park", address: "3300 SE 15th St, Gainesville, FL", desc: "Historic springs park along the Gainesville-Hawthorne Trail. A peaceful local secret.", sentiment: "88% positive", mentions: "94 mentions" },
    { id: 5, name: "Hogtown Creek Headwaters", address: "1520 NW 4th St, Gainesville, FL", desc: "A serene nature preserve winding through residential Gainesville. Underrated and beautiful.", sentiment: "85% positive", mentions: "67 mentions" },
  ],
}


const COMMENTS = [
  { text: "This place is absolutely a hidden gem — been going for 5 years and it never disappoints.", upvotes: 326, source: "r/GNV" },
  { text: "Locals only know about this. Please don't let tourists find out.", upvotes: 218, source: "r/Gainesville" },
  { text: "Stumbled on this by accident and it completely changed my view of GNV.", upvotes: 194, source: "r/GNV" },
  { text: "Way better than anything on the tourist lists. Authentic and affordable.", upvotes: 128, source: "r/Florida" },
]
*/

const ICONS = { restaurants: "🍴", cafes: "☕", attractions: "🌿" }

function GemLogo({ size = 26 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
      <polygon points="16,2 26,10 16,13 6,10" fill="#2ec4b6" fillOpacity="0.9"/>
      <polygon points="6,10 16,13 11,28 2,16" fill="#1a9e92" fillOpacity="0.85"/>
      <polygon points="26,10 30,16 21,28 16,13" fill="#2ec4b6" fillOpacity="0.6"/>
      <polygon points="16,13 21,28 11,28" fill="#23b0a4" fillOpacity="0.75"/>
      <polygon points="16,2 26,10 30,16 21,28 11,28 2,16 6,10" fill="none" stroke="#2ec4b6" strokeWidth="0.75" strokeLinejoin="round"/>
      <line x1="6" y1="10" x2="26" y2="10" stroke="rgba(255,255,255,0.4)" strokeWidth="0.5"/>
      <line x1="6" y1="10" x2="16" y2="13" stroke="rgba(255,255,255,0.3)" strokeWidth="0.5"/>
      <line x1="26" y1="10" x2="16" y2="13" stroke="rgba(255,255,255,0.3)" strokeWidth="0.5"/>
    </svg>
  )
}

function Nav({ onHome }) {
  return (
    <nav className="nav">
      <div className="nav-logo" onClick={onHome}>
        <span className="nav-logo-text">Paraíba</span>
      </div>
    </nav>
  )
}

function BackBtn({ onClick }) {
  return (
    <button className="back" onClick={onClick}>← Back</button>
  )
}

function HomePage({ onExplore }) {
  return (
    <div className="home">
      <div className="fu"><GemLogo size={52} /></div>
      <p className="home-eyebrow fu1">Powered by local Reddit discussions</p>
      <h1 className="home-title fu2">Find the <em>hidden gems</em> of your city.</h1>
      <p className="home-sub fu3">
        We parse thousands of Reddit posts, extract sentiment, and rank local spots that tourists never find.
      </p>
      <button className="home-btn fu4" onClick={onExplore}>Start Exploring</button>
      <div className="home-stats fu5">
        <div className="stat">
          <span className="stat-num">10k+</span>
          <span className="stat-label">Posts Analyzed</span>
        </div>
        <div className="stat">
          <span className="stat-num">r/GNV</span>
          <span className="stat-label">Source Subreddit</span>
        </div>
        <div className="stat">
          <span className="stat-num">Top 5</span>
          <span className="stat-label">Per Category</span>
        </div>
      </div>
    </div>
  )
}

function CategoryPage({ onSelect, onBack }) {
  const cats = [
    { key: "restaurants", label: "Restaurants" },
    { key: "cafes", label: "Cafes" },
    { key: "attractions", label: "Attractions" },
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
function LoadingPage({ label, step }) {
  const steps = [
    { label: "Scraping r/GNV posts", done: step > 0, active: step === 0 },
    { label: `Extracting ${label} mentions`, done: step > 1, active: step === 1 },
    { label: "Running sentiment analysis", done: step > 2, active: step === 2 },
    { label: "Ranking results", done: step > 3, active: step === 3 },
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
          <div key={i} className={`loading-step${s.active ? " active" : ""}${s.done ? " done" : ""}`}>
            <div className="step-dot" />
            {s.done ? "✓ " : ""}{s.label}
          </div>
        ))}
      </div>
    </div>
  )
}
function ResultsPage({ places, category, label, onSelect, onBack }) {
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
          className={`result-card fu${Math.min(i + 1, 5)}${i === 0 ? " top" : ""}`}
          onClick={() => onSelect(p)}
        >
          <div className="result-top-row">
            <span className="result-num">#{p.id}</span>
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

function PlaceMap({ place }) {
  const address = place.address || `${place.name}, Gainesville, FL`
  const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`
  return (
    <div className="detail-map">
      <div className="map-placeholder">
        <span className="map-placeholder-icon">📍</span>
        <span className="map-placeholder-text">Map coming soon</span>
        <span className="map-placeholder-address">{address}</span>
      </div>
      <a className="map-open-btn" href={googleMapsUrl} target="_blank" rel="noopener noreferrer">
        ↗ Open in Google Maps
      </a>
    </div>
  )
}

function DetailPage({ place, label, onBack }) {
  return (
    <>
      <BackBtn onClick={onBack} />
      <p className="detail-breadcrumb fu">{label} / {place.name}</p>
      <div className="detail-card fu1">
        <PlaceMap place={place} />
        <div className="detail-body">
          <p className="detail-cat">{label}</p>
          <h2 className="detail-name">{place.name}</h2>
          <p className="detail-desc">{place.desc}</p>
          <div className="detail-meta">
            <div className="meta-item">
              <span className="meta-label">Sentiment</span>
              <span className="meta-value">{place.sentimentRating ? `${Math.round(place.sentimentRating * 100)}% positive` : "N/A"}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Reddit Mentions</span>
              <span className="meta-value">{place.mentionCount ? `${place.mentionCount} mentions` : "N/A"}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Ranking</span>
              <span className="meta-value">#{place.ranking}</span>
            </div>
          </div>
        </div>
      </div>
      <p className="comments-heading fu2">What locals are saying</p>
      {place.comments && place.comments.length > 0 ? (
        place.comments.map((c, i) => (
          <div key={i} className={`comment-card fu${Math.min(i + 2, 5)}`}>
            <div className="comment-body">
              <span className="comment-text">"{c}"</span>
              <span className="comment-source">r/GNV</span>
            </div>
          </div>
        ))
      ) : (
        <p style={{color: "#9ca3af", fontSize: "13px"}}>No comments yet</p>
      )}
    </>
  )
}

export default function App() {
  const [places, setPlaces] = useState([])
  const [screen, setScreen] = useState("home")
  const [category, setCategory] = useState(null)
  const [label, setLabel] = useState("")
  const [loadStep, setLoadStep] = useState(0)
  const [place, setPlace] = useState(null)

  const goHome = () => { setScreen("home"); setLoadStep(0) }

  const handleCategory = async (cat, lbl) => {
  setCategory(cat); setLabel(lbl); setLoadStep(0)
  setScreen("loading")
  ;[0, 1, 2, 3].forEach(i => {
    setTimeout(() => setLoadStep(i + 1), 500 + i * 500)
  })

  try {
    const keyword = cat === "restaurants" ? "Restaurant"
                  : cat === "cafes" ? "Cafe"
                  : "Attraction"
    const res = await axios.get(`/api/paraiba?category=${keyword}`)
    setPlaces(res.data)
  } catch (err) {
    console.error("Failed to fetch places:", err)
    setPlaces([])
  }

  setTimeout(() => setScreen("results"), 2600)
}

  return (
    <>
      <style>{css}</style>
      <Nav onHome={goHome} />
      <div className="page" key={screen}>
        {screen === "home"     && <HomePage onExplore={() => setScreen("category")} />}
        {screen === "category" && <CategoryPage onSelect={handleCategory} onBack={goHome} />}
        {screen === "loading"  && <LoadingPage label={label} step={loadStep} />}
        {screen === "results" && <ResultsPage places={places} category={category} label={label} onSelect={(p) => { setPlace(p); setScreen("detail") }} onBack={() => setScreen("category")} />}
        {screen === "detail"   && <DetailPage place={place} label={label} onBack={() => setScreen("results")} />}
      </div>
    </>
  )
}