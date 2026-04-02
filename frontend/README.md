Paraíba Frontend

React + Vite frontend for the Paraíba hidden gems recommendation app.

Getting Started

Prerequisites
- Node.js v18+
- Backend API URL configured in environment variables

Install & Run
```bash
cp .env.example .env
npm install
npm run dev
```

Set `VITE_DEV_API_URL` in `.env` for local proxying.
Set `VITE_API_URL` when the frontend should call a separately deployed backend.

Stack

- React 18
- Vite
- Axios

Screens

| Screen | Description |
|---|---|
| Home | Hero with gem logo and stats |
| Category | Choose Restaurants, Cafes, or Attractions |
| Loading | Animated pipeline steps |
| Results | Top 5 ranked places from MongoDB |
| Detail | Place info, map, sentiment, Reddit comments |

API Connection

The app reads its API base URL from environment variables:

- `VITE_DEV_API_URL` for the Vite dev proxy
- `VITE_API_URL` for deployed environments

If `VITE_API_URL` is blank, the frontend will use same-origin `/api` requests.
