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
    display: grid; grid-template-columns: repeat(2, 1fr);
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

export default css
