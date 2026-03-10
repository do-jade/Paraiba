export default function GemLogo({ size = 26 }) {
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
