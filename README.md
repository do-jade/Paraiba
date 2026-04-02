# Project Paraíba
 
**A hidden gem restaurant discovery platform for Gainesville, FL**  
Senior Capstone Project for the University of Florida  
*Adam Popovich · Dohyun Lee · Jimin Kwak · Thomas Hewatt*
 
---

## Overview
 
Project Paraíba surfaces lesser-known but highly-rated dining spots that get overlooked by mainstream review platforms. Rather than relying solely on star ratings, Paraíba combines Reddit community signals, ML/NLP sentiment analysis, and Google Maps data to compute a composite "Paraíba Score" for each restaurant. Our project rewards places that locals genuinely love but haven't yet been flooded with reviews.

### What Makes a Hidden Gem?
 
A restaurant scores well on Paraíba when it has:
- High Google ratings with a low review count
- Authentic, positive Reddit discussion from the local community
- Strong sentiment from NLP analysis, including implicit endorsements that standard tools miss

---
 
## Tech Stack
 
### Backend (Python)
- Python 3.12.x
- NumPy < 2.0 — numerical operations 
- pytest — unit and integration testing
- spaCy 3.7.x : NLP, tokenization, named entity recognition
- VADER Sentiment : Sentiment polarity with custom lexicon boosting
 
### Frontend (JavaScript)
- React 
 
### Database
- MongoDB Atlas : stores Reddit comments collection and destinations collection (sentiment, ranking, and location data)
 
### External APIs
- Google Places API : restaurant ratings and review counts
 
---

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/do-jade/Paraiba.git
cd Paraiba

# Install backend dependencies
cd backend
npm install
cp .env.example .env
```

Backend environment variables:

- `MONGO_URI`
- `APIFY_TOKEN`
- `ALLOWED_ORIGINS`

Run locally:

```bash
npm run dev
```

### Frontend Setup
 
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend environment variables:

- `VITE_DEV_API_URL`
- `VITE_API_URL`

### Vercel Deployment

Deploy `frontend` and `backend` as separate Vercel projects.

- Frontend project root: `frontend`
- Backend project root: `backend`

Set these Vercel environment variables:

- Frontend: `VITE_API_URL=https://<your-backend-domain>`
- Backend: `MONGO_URI`, `APIFY_TOKEN`, `ALLOWED_ORIGINS=https://<your-frontend-domain>`
