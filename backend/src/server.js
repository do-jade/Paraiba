import express from "express";
import notesRoutes from "./routes/notesRoutes.js";
import commentRoutes from "./routes/commentsRoutes.js";
import paraibaRoutes from "./routes/paraibaRoutes.js";
import { connectDB } from "./config/db.js";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001

connectDB();

// middleware
app.use(express.json());

app.use("/api/notes", notesRoutes)
app.use("/api/comments", commentRoutes)
app.use("/api/paraiba", paraibaRoutes)
 
app.listen(PORT, ()=> {
    console.log("Sever started on PORT:", PORT);
})