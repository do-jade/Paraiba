import BackBtn from "../components/BackBtn";
import PlaceMap from "../components/PlaceMap";

export default function DetailPage({ place, label, onBack }) {
  const truncateText = (text, maxLength = 140) => {
    const normalized = String(text).trim();

    if (normalized.length <= maxLength) {
      return normalized;
    }

    return `${normalized.slice(0, maxLength).trimEnd()}...`;
  };

  const rawTypes = Array.isArray(place.categoryType)
    ? place.categoryType
    : typeof place.categoryType === "string"
    ? place.categoryType.split(",")
    : [];

  const displayTypes = rawTypes
    .map((type) => String(type).trim())
    .filter(Boolean)
    .filter((type) => type.toLowerCase() !== "general")
    .slice(0, 4)
    .map((type) =>
      type.split(" ").map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ")
    );

  const sentimentValue = place.sentimentRating ?? place.sentimentrating;
  const googleReviews = Array.isArray(place.googleReviews)
    ? place.googleReviews
        .map((review) => {
          if (typeof review === "string") return review.trim();
          if (review && typeof review === "object" && typeof review.text === "string") {
            return review.text.trim();
          }
          return "";
        })
        .filter(Boolean)
    : [];
  const rawDescription =
    place.description ||
    (place.comments && place.comments.length > 0
      ? `"${place.comments[0].text}"`
      : "No description yet.");
  const description = truncateText(rawDescription);

  const gemScore = place.ranking ? Math.round(place.ranking) : null;
  const sentimentPct = sentimentValue ? Math.round(sentimentValue * 100) : null;

  return (
    <>
      <BackBtn onClick={onBack} />

      {/* ── HERO: name + description left, Gem Score callout right ── */}
      <div className="detail-hero fu">
        <div className="detail-hero-left">
          <p className="detail-cat fu1">{label}</p>
          <h2 className="detail-name fu2">{place.name}</h2>
          {displayTypes.length > 0 && (
            <div className="detail-tag-row fu3">
              {displayTypes.map((type) => (
                <span key={type} className="detail-tag">{type}</span>
              ))}
            </div>
          )}
          <p className="detail-desc fu4">{description}</p>
        </div>

        {/* Gem Score — primary metric, visually dominant out of 70*/}
        <div className="detail-score-callout fu3">
          <span className="detail-score-label">
            Gem Score
            <span className="info-trigger" tabIndex="0" aria-label="How Gem Score is calculated">
              i
              <span className="info-tooltip">
                Calculated from Reddit engagement, sentiment analysis, and Google place quality signals.
              </span>
            </span>
          </span>
          <span className="detail-score-number">{gemScore ?? "—"}</span>
          <span className="detail-score-sub">out of 75</span>
        </div>
      </div>

      {/* ── STATS STRIP: secondary metrics chunked into one scannable row ── */}
      <div className="detail-stats-strip fu4">
        <div className="detail-stat">
          <span className="detail-stat-value">
            {sentimentPct != null ? `${sentimentPct}%` : "—"}
          </span>
          <span className="detail-stat-label">Positive Sentiment</span>
        </div>
        <div className="detail-stat-divider" />
        <div className="detail-stat">
          <span className="detail-stat-value">{place.mentionCount ?? "—"}</span>
          <span className="detail-stat-label">Reddit Mentions</span>
        </div>
        <div className="detail-stat-divider" />
        <div className="detail-stat">
          <span className="detail-stat-value">
            {place.rating ? `${place.rating.toFixed(1)} ★` : "—"}
          </span>
          <span className="detail-stat-label">Google Rating</span>
        </div>
        <div className="detail-stat-divider" />
        <div className="detail-stat">
          <span className="detail-stat-value">{place.reviewCount ?? "—"}</span>
          <span className="detail-stat-label">Google Reviews</span>
        </div>
      </div>
      <div className="detail-section-rule fu5" aria-hidden="true" />

      {/* ── MAP ── */}
      <div className="detail-map-wrap fu5">
        <div className="detail-section-header">
          <p className="comments-heading">Location</p>
        </div>
        <div className="detail-map-section">
          <PlaceMap place={place} />
        </div>
      </div>
      <div className="detail-section-rule" aria-hidden="true" />

      {/* ── REDDIT COMMENTS ── */}
      <div className="detail-comments-section">
        <div className="detail-section-header fu">
          <p className="comments-heading">What locals are saying on Reddit</p>
          {place.link && place.link.length > 0 && (
            <a
              href={place.link[0]}
              target="_blank"
              rel="noopener noreferrer"
              className="detail-link-btn"
            >
              ↗ View on Reddit
            </a>
          )}
        </div>
        {place.comments && place.comments.length > 0 ? (
          <div className="comments-list">
            {place.comments.map((c, i) => (
              <div key={i} className={`comment-card fu${Math.min(i + 2, 5)}`}>
                <div className="comment-quote-mark">"</div>
                <div className="comment-body">
                  <span className="comment-text">{c.text}</span>
                  <span className="comment-source">Local Reddit mention • r/GNV</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="detail-empty">No comments yet</p>
        )}
      </div>

      {/* ── GOOGLE REVIEWS ── */}
      {googleReviews.length > 0 && (
        <>
          <div className="detail-section-rule" aria-hidden="true" />
          <div className="detail-comments-section">
            <div className="detail-section-header fu">
              <p className="comments-heading">Google Reviews</p>
              <div className="google-rating-badge">
                <span className="google-rating-star">★</span>
                <span className="google-rating-value">
                  {place.rating ? place.rating.toFixed(1) : '—'}
                </span>
                {place.reviewCount && (
                  <span className="google-rating-count">({place.reviewCount.toLocaleString()})</span>
                )}
              </div>
            </div>
            <div className="comments-list">
              {googleReviews.map((review, i) => (
                <div key={i} className={`comment-card fu${Math.min(i + 2, 5)}`}>
                  <div className="google-g-badge">G</div>
                  <div className="comment-body">
                    <span className="comment-text">{review}</span>
                    <span className="comment-source">Google Review</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </>
  );
}
