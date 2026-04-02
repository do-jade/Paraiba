import mongoose from "mongoose";

let cachedConnection = null;
let cachedPromise = null;

export const connectDB = async () => {
    if (cachedConnection) {
        return cachedConnection;
    }

    if (!process.env.MONGO_URI) {
        throw new Error("Missing MONGO_URI in environment");
    }

    if (!cachedPromise) {
        cachedPromise = mongoose.connect(process.env.MONGO_URI).then((connection) => {
            console.log("MONGODB Connected Successfully");
            cachedConnection = connection;
            return connection;
        });
    }

    try {
        return await cachedPromise;
    }
    catch (error) {
        cachedPromise = null;
        console.error("Error connecting to MONGODB", error);
        throw error;
    }
};
