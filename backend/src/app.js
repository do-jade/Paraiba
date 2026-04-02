import express from "express";
import cors from "cors";

import notesRoutes from "./routes/notesRoutes.js";
import paraibaRoutes from "./routes/paraibaRoutes.js";
import commentRoutes from "./routes/commentsRoutes.js";

const app = express();

const allowedOrigins = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((origin) => origin.trim())
  .filter(Boolean);

app.use(
  cors({
    origin(origin, callback) {
      if (!origin || allowedOrigins.length === 0 || allowedOrigins.includes(origin)) {
        return callback(null, true);
      }

      return callback(new Error("Not allowed by CORS"));
    },
  }),
);

app.use(express.json());

app.get("/api/health", (_req, res) => {
  res.status(200).json({ ok: true });
});

app.use("/api/notes", notesRoutes);
app.use("/api/comments", commentRoutes);
app.use("/api/paraiba", paraibaRoutes);

export default app;
