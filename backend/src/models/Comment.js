import mongoose from "mongoose";

// 1- create a schema 
// 2- model based off of that schema

const commentSchema = new mongoose.Schema(
    {
        comment_text: {
            type: String,
            required: true
        },
        upvotes: {
            type: Number,
            required: true
        },
        link: {
            type: String,
            required: true
        },
        processed: {
            type: Boolean,
            default: false,
            required: true
        },
    },
    { timestamps: true} // createdAt, updatedAt 
);

const Comment = mongoose.model("Comment", commentSchema)

export default Comment