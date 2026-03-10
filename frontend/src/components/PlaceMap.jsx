export default function PlaceMap({ place }) {
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
