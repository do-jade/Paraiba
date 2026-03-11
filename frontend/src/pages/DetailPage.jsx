import BackBtn from "../components/BackBtn";
import PlaceMap from "../components/PlaceMap";

export default function DetailPage({ place, label, onBack }) {
  console.log("place:", place)
console.log("comments:", place.comments)
console.log("isArray:", Array.isArray(place.comments))
console.log("length:", place.comments?.length)
  return (
    <>
      <BackBtn onClick={onBack} />
      <p className="detail-breadcrumb fu">
        {label} / {place.name}
      </p>
      <div className="detail-card fu1">
        <PlaceMap place={place} />
        <div className="detail-body">
          <p className="detail-cat">{label}</p>
          <h2 className="detail-name">{place.name}</h2>
          <p className="detail-desc">{place.description}</p>
          <div className="detail-meta">
            <div className="meta-item">
              <span className="meta-label">Sentiment</span>
              <span className="meta-value">
                {place.sentimentrating
                  ? `${Math.round(place.sentimentrating * 100)}% positive`
                  : "N/A"}
              </span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Reddit Mentions</span>
              <span className="meta-value">
                {place.mentionCount ? `${place.mentionCount} mentions` : "N/A"}
              </span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Ranking</span>
              <span className="meta-value">#{place.ranking}</span>
            </div>
          </div>
        </div>
      </div>
      <p className="comments-heading fu2">What locals are saying on reddit</p>
      {place.comments && place.comments.length > 0 ? (
        place.comments.map((c, i) => (
          <div key={i} className={`comment-card fu${Math.min(i + 2, 5)}`}>
            <div className="comment-body">
              <span className="comment-text">"{c.text}"</span>
              <span className="comment-source">r/GNV</span>
            </div>
          </div>
        ))
      ) : (
        <p style={{ color: "#9ca3af", fontSize: "13px" }}>No comments yet</p>
      )}
    </>
  );
}
