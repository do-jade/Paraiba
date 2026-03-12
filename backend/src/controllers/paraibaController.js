import Paraiba from "../models/Paraiba.js";

export async function createParaibaEntry(req, res) {
  try {
    const {
      name,
      address,
      category,
      cuisineType,
      reviewCount,
      rating,
      description,
      sentimentRating,
      ranking,
      upvotes,
      mentionCount,
      location,
      comments,
      googleReviews,
      link,
      servesBreakfast,
      servesBrunch,
      servesLunch,
      servesDinner,
      servesBeer,
      servesWine,
      servesVegetarian,
      dineIn,
      takeout,
      delivery,
    } = req.body;

    const entry = new Paraiba({
      name,
      address,
      category,
      cuisineType,
      reviewCount,
      rating,
      description,
      sentimentRating,
      ranking,
      upvotes,
      mentionCount,
      location,
      comments,
      googleReviews,
      link,
      servesBreakfast,
      servesBrunch,
      servesLunch,
      servesDinner,
      servesBeer,
      servesWine,
      servesVegetarian,
      dineIn,
      takeout,
      delivery,
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

// Jimin
export async function getParaibaEntries(req, res) {
  try {
    const { category } = req.query;
    let query = {};

    if (category) {
      const normalizedCategory = category.toLowerCase();

      if (normalizedCategory === "restaurant") {
        query = {
          $or: [
            { category: { $regex: "restaurant", $options: "i" } },
            { category: { $regex: "food", $options: "i" } },
          ],
        };
      } else if (normalizedCategory === "attraction") {
        query = {
          $and: [
            {
              $or: [
                { category: { $regex: "establishment", $options: "i" } },
                { category: { $regex: "attraction", $options: "i" } },
              ],
            },
            {
              category: { $not: /restaurant|food/i },
            },
          ],
        };
      } else {
        query = {
          category: { $regex: category, $options: "i" },
        };
      }
    }

    const entries = await Paraiba.find(query).sort({ ranking: -1 }).limit(5);
    console.log(entries);
    return res.status(200).json(entries);
  } catch (error) {
    console.log("Error in getParaibaEntries controller", error);
    return res.status(500).json({ message: "Internal server error" });
  }
}
