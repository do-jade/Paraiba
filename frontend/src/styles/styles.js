// Main app styles are kept here and injected from App.jsx.
const css = `
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html, body, #root { width: 100%; height: 100%; }
  body { background: #faf9f6; font-family: 'Manrope', sans-serif; color: #1a1a2e; -webkit-font-smoothing: antialiased; }

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
    background: rgba(250,249,246,0.9);
    backdrop-filter: blur(20px);
  }
  .nav-logo {
    display: flex; align-items: center; gap: 9px;
    cursor: pointer; user-select: none;
  }
  .nav-logo-text {
    font-family: 'Manrope', sans-serif;
    font-size: 20px; font-weight: 600;
    letter-spacing: 0.01em; color: #1a1a2e;
    line-height: 1;
  }

  /* ── PAGE ── */
  .page {
    width: 100%; max-width: 940px;
    margin: 0 auto;
    padding: 100px 28px 80px;
    min-height: 100vh;
    display: flex; flex-direction: column; align-items: center;
  }

  /* ── BACK BTN ── */
  .back {
    display: flex; align-items: center; gap: 8px;
    background: none; border: none; cursor: pointer;
    font-family: 'Manrope', sans-serif;
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
    font-family: 'Manrope', sans-serif;
    font-size: clamp(28px, 6vw, 48px); font-weight: 900;
    line-height: 1.1; color: #1a1a2e; margin-bottom: 18px;
    white-space: normal; word-break: break-word;
  }
  .home-title em { font-style: normal; color: #2ec4b6; font-weight: 700; }
  .home-sub {
    font-size: 14px; color: #6b7280; line-height: 1.8;
    max-width: 360px; font-weight: 300; margin-bottom: 36px;
  }
  .home-btn {
    padding: 15px 48px; background: #1a1a2e; color: #f7f6f2;
    border: none; border-radius: 12px;
    font-family: 'Manrope', sans-serif;
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
    font-family: 'Manrope', sans-serif;
    font-size: 22px; font-weight: 700; color: #1a1a2e;
    display: block; line-height: 1; letter-spacing: 0.04em;
  }
  .stat-label {
    font-size: 10px; font-weight: 500; letter-spacing: 0.12em;
    text-transform: uppercase; color: #9ca3af; margin-top: 4px;
    display: block;
  }

  /* ── CATEGORY ── */
  .cat-header { text-align: center; margin-bottom: 36px; width: 100%; }
  .cat-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 0.2em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 10px;
  }
  .cat-title {
    font-family: 'Manrope', sans-serif;
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
  .cat-sublabel {
    font-size: 11px; font-weight: 400; color: #9ca3af;
    text-align: center; line-height: 1.4;
    letter-spacing: 0; text-transform: none;
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
    font-family: 'Manrope', sans-serif;
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
  .results-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 0.2em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 8px;
  }
  .results-title {
    font-family: 'Manrope', sans-serif;
    font-size: 28px; font-weight: 900; color: #1a1a2e;
  }
  .result-card {
    width: 100%; background: #fff; border-radius: 14px;
    padding: 18px 22px 20px; margin-bottom: 10px;
    display: flex; flex-direction: column; gap: 8px;
    cursor: pointer; border: 1.5px solid #ece9e1;
    transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
  }
  .result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
    border-color: #2ec4b6;
  }
  .results-title span { font-style: normal; color: #2ec4b6; }
  .result-name {
    font-size: 16px; font-weight: 600; color: #1a1a2e; line-height: 1.3;
    margin-bottom: 0;
  }
  .result-header-row {
    display: flex; justify-content: space-between; align-items: flex-start;
    gap: 14px;
  }
  .result-score-line {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #2ec4b6;
    flex-shrink: 0;
    margin-top: 2px;
    text-align: right;
  }
  .result-meta-row {
    display: flex; align-items: center; gap: 8px;
    flex-wrap: wrap;
  }
  .result-meta-row.bottom {
    margin-top: 2px;
  }
  .result-chip {
    display: inline-flex; align-items: center;
    padding: 4px 9px; border-radius: 999px;
    background: rgba(26,26,46,0.06); color: #1a1a2e;
    font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .result-chip.subtle {
    background: rgba(46,196,182,0.09);
    color: #356b69;
    font-weight: 600;
    letter-spacing: 0.05em;
  }
  .result-meta-text {
    font-size: 11px; color: #7b8190; font-weight: 500;
    letter-spacing: 0.02em;
  }
  .result-desc {
    font-size: 12px; color: #6b7280; line-height: 1.75; font-weight: 300;
  }
  .result-cta {
    display: inline-flex; align-items: center; justify-content: center;
    align-self: flex-end; margin-top: 6px;
    padding: 8px 12px; border-radius: 12px;
    background: #1a1a2e; color: #f7f6f2;
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: transform 0.18s, background 0.18s, box-shadow 0.18s;
  }
  .result-card:hover .result-cta {
    background: #2ec4b6;
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(46,196,182,0.22);
  }
  .error-state {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; gap: 16px;
  }
  .error-icon { font-size: 40px; }
  .error-title { font-family: 'Manrope', sans-serif; font-size: 22px; font-weight: 900; color: #1a1a2e; }
  .error-sub { font-size: 13px; color: #6b7280; font-weight: 300; }
  .error-btn {
    margin-top: 8px; padding: 12px 32px;
    background: #1a1a2e; color: #f7f6f2; border: none;
    border-radius: 12px; font-family: 'Manrope', sans-serif;
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; cursor: pointer;
  }

  /* ── DETAIL ── */

  /* Hero: two-column — left text block, right Gem Score */
  .detail-hero {
    width: 100%; display: flex; align-items: flex-start;
    gap: 28px; margin-bottom: 20px;
  }
  .detail-hero-left {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column;
  }
  .detail-cat {
    font-size: 10px; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #2ec4b6; margin-bottom: 10px;
  }
  .detail-name {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(26px, 4vw, 40px); font-weight: 900; color: #1a1a2e;
    letter-spacing: -0.03em;
    line-height: 1.08; margin-bottom: 14px;
  }
  .detail-tag-row {
    display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px;
  }
  .detail-tag {
    display: inline-flex; align-items: center;
    padding: 5px 11px; border-radius: 999px;
    background: rgba(46,196,182,0.1); color: #356b69;
    font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .detail-desc {
    font-size: 14px; color: #6b7280; line-height: 1.9; font-weight: 300;
  }

  /* Gem Score callout — primary metric, visually dominant */
  .detail-score-callout {
    flex-shrink: 0; width: 158px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 4px;
    padding: 22px 18px 18px;
    background: rgba(255,255,255,0.92); border-radius: 20px;
    border: 1.5px solid rgba(46,196,182,0.22);
    box-shadow: 0 8px 20px rgba(26,26,46,0.04);
    text-align: center;
  }
  .detail-score-label {
    font-size: 9px; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #9ca3af;
    margin-bottom: 6px;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .detail-score-number {
    font-family: 'Manrope', sans-serif;
    font-size: 56px; font-weight: 900; line-height: 1;
    color: #1a1a2e; letter-spacing: -0.04em;
  }
  .detail-score-sub {
    font-size: 10px; color: #9ca3af; font-weight: 500;
    letter-spacing: 0.04em; margin-top: 2px;
    text-transform: uppercase;
  }

  /* Info tooltip */
  .info-trigger {
    position: relative;
    display: inline-flex; align-items: center; justify-content: center;
    width: 16px; height: 16px; border-radius: 50%;
    background: rgba(26,26,46,0.08); color: #6b7280;
    font-size: 10px; font-weight: 700; line-height: 1;
    text-transform: none; letter-spacing: 0;
    cursor: help; outline: none;
  }
  .info-tooltip {
    position: absolute; left: 50%; bottom: calc(100% + 10px);
    transform: translateX(-50%) translateY(4px);
    width: 220px; padding: 10px 12px; border-radius: 10px;
    background: #1a1a2e; color: #f7f6f2;
    font-size: 11px; font-weight: 500; line-height: 1.45;
    text-transform: none; letter-spacing: 0.01em;
    box-shadow: 0 14px 28px rgba(26,26,46,0.18);
    opacity: 0; pointer-events: none;
    transition: opacity 0.16s, transform 0.16s; z-index: 10;
  }
  .info-tooltip::after {
    content: ''; position: absolute; left: 50%; top: 100%;
    transform: translateX(-50%);
    border-left: 6px solid transparent; border-right: 6px solid transparent;
    border-top: 6px solid #1a1a2e;
  }
  .info-trigger:hover .info-tooltip,
  .info-trigger:focus .info-tooltip { opacity: 1; transform: translateX(-50%) translateY(0); }

  /* Stats strip — secondary metrics in one scannable horizontal band */
  .detail-stats-strip {
    width: 100%; background: #fff;
    border: 1.5px solid #ece9e1; border-radius: 16px;
    padding: 22px 24px;
    display: flex; align-items: center;
    overflow-x: auto;
  }
  .detail-stat {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column;
    align-items: center; gap: 5px;
    text-align: center; padding: 0 10px;
  }
  .detail-stat-value {
    font-size: 20px; font-weight: 700; color: #1a1a2e;
    line-height: 1; letter-spacing: -0.02em; white-space: nowrap;
  }
  .detail-stat-label {
    font-size: 9px; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #9ca3af;
  }
  .detail-stat-divider {
    width: 1px; align-self: stretch; background: #ece9e1;
    flex-shrink: 0; margin: 4px 0;
  }

  .detail-section-rule {
    width: 100%;
    height: 1px;
    margin: 24px 0;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(26,26,46,0.06) 12%,
      rgba(26,26,46,0.06) 88%,
      transparent 100%
    );
  }

  /* Map */
  .detail-map-wrap {
    width: 100%;
  }
  .detail-map-section {
    width: 100%; border-radius: 16px; overflow: hidden;
    border: 1.5px solid #ece9e1;
  }
  .detail-map {
    width: 100%; height: 240px;
    position: relative; overflow: hidden; background: #e4f4f3;
  }
  .map-frame {
    width: 100%; height: 100%;
    border: 0; display: block;
    filter: saturate(0.9) contrast(1.02);
  }
  .map-overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(
      180deg,
      rgba(250,249,246,0.22) 0%,
      rgba(250,249,246,0) 24%,
      rgba(26,26,46,0) 70%,
      rgba(26,26,46,0.12) 100%
    );
  }
  .map-address-badge {
    position: absolute; top: 12px; left: 50%;
    transform: translateX(-50%);
    max-width: calc(100% - 24px);
    background: rgba(250,249,246,0.94);
    color: #1a1a2e; border: 1px solid rgba(236,233,225,0.95);
    border-radius: 999px; padding: 9px 14px;
    font-size: 11px; font-weight: 600; line-height: 1.3;
    box-shadow: 0 8px 18px rgba(26,26,46,0.08);
    backdrop-filter: blur(10px);
    text-align: center;
  }
  .map-open-btn {
    position: absolute; bottom: 12px; right: 12px;
    background: #1a1a2e; color: #f7f6f2;
    font-family: 'Manrope', sans-serif;
    font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; border: none; border-radius: 12px;
    padding: 10px 16px; cursor: pointer;
    transition: transform 0.18s, background 0.18s, box-shadow 0.18s;
    text-decoration: none; display: flex; align-items: center; gap: 6px;
    box-shadow: 0 10px 22px rgba(26,26,46,0.16);
  }
  .map-open-btn:hover {
    background: #2ec4b6;
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(46,196,182,0.24);
  }

  /* Comments */
  .detail-comments-section { width: 100%; }
  .detail-section-header {
    width: 100%; display: flex; justify-content: space-between; align-items: center;
    gap: 16px; margin-bottom: 16px;
  }
  .comments-heading {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #9ca3af; line-height: 1;
  }
  .detail-link-btn {
    display: inline-flex; align-items: center; justify-content: center;
    padding: 10px 18px; border-radius: 12px;
    background: #1a1a2e; color: #f7f6f2;
    font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; text-decoration: none;
    transition: transform 0.18s, background 0.18s, box-shadow 0.18s; line-height: 1;
  }
  .detail-link-btn:hover {
    background: #2ec4b6; transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(46,196,182,0.22);
  }
  .comments-list { width: 100%; display: flex; flex-direction: column; gap: 10px; }
  .comment-card {
    width: 100%; background: #fff; border-radius: 14px;
    padding: 18px 20px;
    display: flex; align-items: flex-start; gap: 16px;
    border: 1.5px solid #ece9e1;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  }
  .comment-card:hover {
    border-color: rgba(46,196,182,0.4); transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(26,26,46,0.05);
  }
  .comment-quote-mark {
    font-family: 'Manrope', sans-serif;
    font-size: 36px; line-height: 1; color: rgba(46,196,182,0.4);
    flex-shrink: 0; margin-top: -4px;
  }
  .comment-body { display: flex; flex-direction: column; gap: 8px; flex: 1; }
  .comment-text { font-size: 14px; color: #374151; line-height: 1.8; font-weight: 300; }
  .comment-source { font-size: 10px; color: #9ca3af; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
  .detail-empty { color: #9ca3af; font-size: 13px; align-self: flex-start; }

  /* ── RESULTS LAYOUT ── */
  .results-layout {
    display: flex; gap: 20px; width: 100%; align-items: flex-start;
  }
  .results-sidebar-wrap {
    width: 240px; flex-shrink: 0;
    position: sticky; top: 90px;
    align-self: flex-start;
  }
  .results-main {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column;
  }
  .results-header {
    width: 100%; text-align: center; margin-bottom: 36px;
  }
  .results-filter-hint {
    font-size: 11px; color: #2ec4b6; font-weight: 600;
    margin-top: 6px; letter-spacing: 0.04em;
  }

  /* ── SIDEBAR ── */
  .results-sidebar {
    display: flex; flex-direction: column; gap: 16px;
  }
  .sidebar-section { display: flex; flex-direction: column; gap: 10px; }
  .sidebar-section-header {
    display: flex; justify-content: space-between; align-items: center;
  }
  .sidebar-section-label {
    font-size: 9px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #9ca3af;
  }
  .sidebar-clear-btn {
    background: none; border: none; cursor: pointer;
    font-family: 'Manrope', sans-serif;
    font-size: 10px; font-weight: 600; color: #2ec4b6;
    padding: 0; transition: opacity 0.2s;
  }
  .sidebar-clear-btn:hover { opacity: 0.7; }

  /* Dropdown */
  .sidebar-select-wrap {
    position: relative; width: 100%;
  }
  .sidebar-select {
    width: 100%; padding: 10px 32px 10px 12px;
    background: #fff; border: 1.5px solid #ece9e1;
    border-radius: 10px; cursor: pointer;
    font-family: 'Manrope', sans-serif;
    font-size: 13px; font-weight: 600; color: #1a1a2e;
    appearance: none; -webkit-appearance: none;
    transition: border-color 0.15s;
  }
  .sidebar-select:focus { outline: none; border-color: #2ec4b6; }
  .sidebar-select-arrow {
    position: absolute; right: 12px; top: 50%;
    transform: translateY(-50%);
    font-size: 11px; color: #9ca3af; pointer-events: none;
  }

  /* Group cards */
  .sidebar-group-card {
    background: #fff; border: 1.5px solid #ece9e1;
    border-radius: 12px; padding: 12px 10px 8px;
    display: flex; flex-direction: column; gap: 8px;
  }
  .sidebar-group-title {
    font-size: 9px; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #2ec4b6;
    margin-bottom: 4px; padding-bottom: 6px;
    border-bottom: 1px solid #f0ede6;
  }
  .sidebar-filter-list {
    display: flex; flex-wrap: wrap; gap: 8px;
  }
  .sidebar-filter-list.checkbox-list {
    flex-direction: column;
    gap: 6px;
  }
  .sidebar-filter-item {
    display: inline-flex; align-items: center; justify-content: flex-start;
    min-height: 0; padding: 0; border-radius: 999px;
    background: #fff; border: 1.5px solid #ece9e1; cursor: pointer;
    font-family: 'Manrope', sans-serif;
    font-size: 11px; font-weight: 500; color: #6b7280;
    text-align: left; transition: border-color 0.15s, background 0.15s, box-shadow 0.15s, color 0.15s;
    width: auto;
  }
  .sidebar-filter-item.checkbox-item {
    width: 100%;
    border-radius: 10px;
  }
  .sidebar-filter-pill {
    display: inline-flex; align-items: center; gap: 6px;
    width: auto; max-width: 100%;
    padding: 8px 12px; border-radius: 999px;
    transition: background 0.15s, color 0.15s;
  }
  .sidebar-filter-item.checkbox-item .sidebar-filter-pill {
    width: 100%;
    padding: 10px 12px;
    border-radius: 10px;
    gap: 10px;
  }
  .sidebar-filter-item:hover {
    border-color: rgba(46,196,182,0.36);
    background: #f7f6f2;
  }
  .sidebar-filter-item:hover .sidebar-filter-pill { color: #1a1a2e; }
  .sidebar-filter-item.active {
    border-color: rgba(46,196,182,0.42);
    background: rgba(46,196,182,0.08);
    box-shadow: inset 0 0 0 1px rgba(46,196,182,0.08);
  }
  .sidebar-filter-item.active .sidebar-filter-pill { color: #1a1a2e; font-weight: 600; }
  .sidebar-filter-label { min-width: 0; line-height: 1; white-space: nowrap; }
  .sidebar-filter-check { flex-shrink: 0; font-size: 11px; color: #2ec4b6; font-weight: 700; line-height: 1; }
  .sidebar-checkbox-box {
    width: 16px; height: 16px;
    display: inline-flex; align-items: center; justify-content: center;
    border-radius: 4px;
    border: 1.5px solid #d8d5cd;
    background: #fff;
    color: transparent;
    font-size: 10px; font-weight: 700; line-height: 1;
    flex-shrink: 0;
    transition: border-color 0.15s, background 0.15s, color 0.15s;
  }
  .sidebar-checkbox-box.active {
    border-color: #2ec4b6;
    background: rgba(46,196,182,0.12);
    color: #2ec4b6;
  }

  /* Mobile filter controls — hidden on desktop, shown responsively */
  .mobile-filter-btn { display: none; }
  .mobile-sidebar-drawer { display: none; }

  /* ── RESPONSIVE ── */

  /* Tablet & large phones: 480px – 768px */
  @media (max-width: 768px) {
    .page { padding: 88px 22px 64px; }

    /* Home */
    .home-eyebrow { font-size: 9px; }
    .home-sub { font-size: 13px; max-width: 300px; }
    .home-stats { gap: 28px; margin-top: 40px; padding-top: 32px; }
    .stat-num { font-size: 18px; }

    /* Category */
    .cat-title { font-size: 24px; }
    .cat-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .cat-card { padding: 28px 14px 22px; }

    /* Results — collapse sidebar into drawer */
    .results-sidebar-wrap { display: none; }
    .results-layout { flex-direction: column; }
    .results-title { font-size: 24px; }
    .mobile-filter-btn {
      display: flex; align-items: center; gap: 6px;
      align-self: flex-start; margin-bottom: 14px;
      padding: 9px 18px; border-radius: 20px;
      background: #fff; border: 1.5px solid #ece9e1;
      font-family: 'Manrope', sans-serif;
      font-size: 11px; font-weight: 600; color: #1a1a2e;
      cursor: pointer; transition: border-color 0.2s;
    }
    .mobile-filter-btn:hover { border-color: #2ec4b6; }
    .mobile-sidebar-drawer {
      display: block; width: 100%; margin-bottom: 16px;
    }

    /* Detail page — keep side-by-side, just smaller */
    .detail-hero { gap: 14px; }
    .detail-score-callout {
      width: 110px; flex-shrink: 0;
      padding: 16px 12px 14px;
      border-radius: 16px;
    }
    .detail-score-number { font-size: 38px; }
    .detail-score-sub { font-size: 9px; }
    .detail-score-label { font-size: 8px; margin-bottom: 4px; }
    .detail-stats-strip { gap: 0; padding: 18px; }
    .detail-stat { padding: 0 8px; }
    .detail-stat-value { font-size: 17px; }
    .detail-section-header { flex-direction: column; align-items: flex-start; gap: 10px; }
    .detail-link-btn { align-self: flex-start; }
    .comment-card { padding: 16px 18px; gap: 12px; }
    .loading-steps { width: 100%; max-width: 260px; }
  }

  /* Small phones: up to 480px */
  @media (max-width: 480px) {
    .page { padding: 82px 16px 56px; }

    /* Nav */
    .nav { padding: 16px 20px; }
    .nav-logo-text { font-size: 18px; }

    /* Home */
    .home { gap: 0; padding-top: 10px; }
    .home-eyebrow { font-size: 9px; letter-spacing: 0.16em; margin-bottom: 14px; }
    .home-sub { font-size: 13px; max-width: 280px; margin-bottom: 28px; }
    .home-btn { padding: 13px 36px; font-size: 11px; }
    .home-stats { gap: 20px; margin-top: 36px; padding-top: 28px; }
    .stat-num { font-size: 16px; }
    .stat-label { font-size: 9px; }

    /* Category */
    .cat-title { font-size: 22px; }
    .cat-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
    .cat-card { padding: 22px 10px 18px; gap: 10px; border-radius: 12px; }
    .cat-icon-wrap { width: 48px; height: 48px; font-size: 19px; }
    .cat-label { font-size: 10px; }

    /* Loading */
    .loading-title { font-size: 20px; }
    .loading-steps { width: 100%; padding: 0 8px; }

    /* Results */
    .results-title { font-size: 22px; }
    .result-card { padding: 16px 18px 18px; border-radius: 12px; }
    .result-name { font-size: 15px; }
    .result-desc { font-size: 11px; }

    /* Detail */
    .detail-name { font-size: clamp(20px, 6vw, 28px); }
    .detail-score-callout { width: 96px; padding: 14px 10px 12px; border-radius: 14px; }
    .detail-score-number { font-size: 32px; }
    .detail-score-label { font-size: 7px; }
    .detail-score-sub { font-size: 8px; }
    .detail-stats-strip { padding: 14px 12px; }
    .detail-stat { padding: 0 6px; }
    .detail-stat-value { font-size: 15px; }
    .detail-stat-label { font-size: 8px; }
    .detail-map { height: 200px; }
    .comment-card { padding: 14px 14px; gap: 10px; }
    .comment-text { font-size: 13px; }
    .comment-quote-mark { font-size: 28px; }

    /* Back button */
    .back { margin-bottom: 28px; }
  }
`

export default css