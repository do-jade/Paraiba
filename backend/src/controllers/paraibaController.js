import Paraiba from "../models/Paraiba.js";

export async function createParaibaEntry(req, res) {
  try {
    const {
      name,
      address,
      category,
      reviewCount,
      rating,
      description,
      sentimentRating,
      ranking,
      upvotes,
      comments,
      googleReviews,
      link,
    } = req.body;

    const entry = new Paraiba({
      name,
      address,
      category,
      reviewCount,
      rating,
      description,
      sentimentRating,
      ranking,
      upvotes,
      comments,
      googleReviews,
      link,
    });
    const savedEntry = await entry.save();

    return res.status(201).json({
      message: "Entry created successfully",
      entry: savedEntry,
    });
  } catch (error) {
    console.log("Error in createParaibaEntry controller", error);
    return res.status(500).json({ message: "Internal server error" });
  }
}
