import mongoose from "mongoose";

// 1- create a schema
// 2- model based off of that schema

const paraibaSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    address: {
      type: String,
      required: false,
    },
    category: {
      type: String,
      required: false,
    },
    reviewCount: {
      type: Number,
      required: false,
      min: 0,
    },
    rating: {
      type: Number,
      required: false,
    },
    description: {
      type: String,
      required: false,
    },
    sentimentRating: {
      type: Number,
      required: false,
    },
    ranking: {
      type: Number,
      required: false,
    },
    upvotes: {
      type: Number,
      required: false,
      min: 0,
    },
    comments: {
      type: [String],
      required: false,
      default: [],
    },
    googleReviews: {
      type: [String],
      required: false,
      default: [],
    },
    link: {
      type: String,
      required: false,
    },
  },
  { timestamps: true }, //createdAt, updatedAt
);

const Paraiba = mongoose.model("Paraiba", paraibaSchema);

export default Paraiba;
