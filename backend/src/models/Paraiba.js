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
    cuisineType: {
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
    mentionCount: {
      type: Number,
      required: false,
      min: 0,
    },
    location: {
      type: String,
      required: false,
    },
    comments: {
      type: [
        {
          text: {
            type: String,
            required: true,
          },
        },
      ],
      required: false,
      default: []
    },
    googleReviews: {
      type: [String],
      required: false,
      default: [],
    },
    link: {
      type: [String],
      required: false,
      default: [],
    },
    servesBreakfast: {
      type: Boolean,
      required: false,
    },
    servesBrunch: {
      type: Boolean,
      required: false,
    },
    servesLunch: {
      type: Boolean,
      required: false,
    },
    servesDinner: {
      type: Boolean,
      required: false,
    },
    servesBeer: {
      type: Boolean,
      required: false,
    },
    servesWine: {
      type: Boolean,
      required: false,
    },
    servesVegetarian: {
      type: Boolean,
      required: false,
    },
    dineIn: {
      type: Boolean,
      required: false,
    },
    takeout: {
      type: Boolean,
      required: false,
    },
    delivery: {
      type: Boolean,
      required: false,
    },
  },
  { timestamps: true }, //createdAt, updatedAt
);

const Paraiba = mongoose.model("Paraiba", paraibaSchema);

export default Paraiba;
