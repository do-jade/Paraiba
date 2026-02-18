import express from "express"
import {createParaibaEntry} from "../controllers/paraibaController.js";

const router = express.Router();

router.post("/", createParaibaEntry);

export default router