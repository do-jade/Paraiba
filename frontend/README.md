Paraíba Frontend

React + Vite frontend for the Paraíba hidden gems recommendation app.

Getting Started

Prerequisites
- Node.js v18+
- Backend server running on port 5001

Install & Run
```bash
npm install
npm run dev
```

App runs on `http://localhost:5173`

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

The app proxies all `/api` requests to `http://localhost:5001` via Vite's dev proxy. Make sure the backend is running before starting the frontend.
