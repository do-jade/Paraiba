import math

# Top-level weights for each group (must sum to 1.0)
redditWeight  = 0.40   # Reddit mention count + average upvotes
mlWeight      = 0.20   # VADER sentiment score
googleWeight  = 0.40   # Google rating + review count

# Within the Google group (must sum to 1.0)
googleRatingWeight    = 0.60  # higher rating = better
googleObscurityWeight = 0.40  # fewer reviews = more hidden

# Review count ceiling for obscurity normalization where a place above this count will score 0 on obscurity.
reviewCeiling = 1000

# Reddit normalization ceilings, which will be modified after seeing real data.
mentionCeiling  = 50  
upvoteCeiling   = 200  

# Calculates the Reddit Score portion of the ranking model.
def redditScore(mentionCount: int, upvoteCount: float) -> float:
    mentionLog     = math.log(mentionCount + 1)
    ceilingLog     = math.log(mentionCeiling + 1)
    mentionNorm    = min(1.0, mentionLog / ceilingLog)

    upvoteLog      = math.log(upvoteCount + 1)
    upvoteCeilLog  = math.log(upvoteCeiling + 1)
    upvoteNorm     = min(1.0, upvoteLog / upvoteCeilLog)

    return round((mentionNorm + upvoteNorm) / 2, 4)

# Calculates the ML Score portion of the ranking model.
def mlScore(sentimentScore: float) -> float:
    return round(sentimentScore, 4)

# Calculates Google Score portion of the ranking model.
def googleScore(googleRating: float, googleReviews: int) -> float:
    hiddenGemBonus = 0.1

    ratingNorm = googleRating / 5.0

    reviewLog      = math.log(googleReviews + 1)
    ceilingLog     = math.log(reviewCeiling + 1)
    obscurityScore = max(0.0, 1.0 - (reviewLog / ceilingLog))

    gScore = (googleRatingWeight * ratingNorm) + (googleObscurityWeight * obscurityScore)

    # Hidden gem bonus: high quality but very few reviews
    if googleReviews < 500 and googleRating > 4.5:
        gScore += hiddenGemBonus
        
    # cap at 1.0 to prevent overflow
    gScore = min(1.0, gScore)  
    return round(gScore, 4)


def paraibaScore(
    googleRating: float,
    googleReviews: int,
    redditMentions: int,
    averageUpvotes: float,
    sentimentScore: float,
) -> dict:

    rScore = redditScore(redditMentions, averageUpvotes)
    mScore = mlScore(sentimentScore)
    gScore = googleScore(googleRating, googleReviews)

    initialScore = (
        redditWeight * rScore +
        mlWeight     * mScore +
        googleWeight * gScore
    )

    finalScore = round(initialScore * 100, 2)

    return {
        "Paraíba Score": finalScore,
        "Reddit Score":  rScore,
        "ML Score":      mScore,
        "Google Score":  gScore,
    }


def scoreDestinations(destinations: list[dict]) -> list[dict]:
    """
    Scores a list of destination dicts and returns them sorted highest to lowest.
    """
    results = []
    for destination in destinations:
        try:
            scoreResult = paraibaScore(
                googleRating=destination["googleRating"],
                googleReviews=destination["googleReviews"],
                redditMentions=destination["redditMentions"],
                averageUpvotes=destination["averageUpvotes"],
                sentimentScore=destination["sentimentScore"],
            )

        except (KeyError, ValueError) as e:
            scoreResult = {
                "Paraíba Score": 0.0,
                "Reddit Score": None,
                "ML Score": None,
                "Google Score": None,
                "error": str(e),
            }

        results.append({**destination, "Score Result": scoreResult})

    results.sort(key=lambda x: x["Score Result"]["Paraíba Score"], reverse=True)
    return results

# Testing samples from real locations in GNV. 
if __name__ == "__main__":
    testDestinations = [
        {
            "name": "Gyros Plus",
            "googleRating": 4.6,        
            "googleReviews": 832,
            "redditMentions": 3,
            "averageUpvotes": 52.7,
            "sentimentScore": 0.374,    # avg of comments 1 (0.000) + 37 (0.747)
        },

        {
            "name": "Pearl's Country Store",
            "googleRating": 4.6,
            "googleReviews": 3043,
            "redditMentions": 3,
            "averageUpvotes": 57.7,
            "sentimentScore": 0.750,    # avg of comments 6 (1.000) + 14 (0.807) + 40 (0.444)
        },

        {
            "name": "Caribbean Spice",
            "googleRating": 4.2,
            "googleReviews": 529,
            "redditMentions": 3,
            "averageUpvotes": 42.7,
            "sentimentScore": 0.524,    # avg of comments 14 (0.807) + 30 (0.765) + 33 (0.000)
        },

        {
            "name": "Mac's Drive Thru",
            "googleRating": 4.7,        
            "googleReviews": 1484,
            "redditMentions": 3,
            "averageUpvotes": 10.0,
            "sentimentScore": 0.546,    # avg of comments 5 (1.000) + 16 (0.000) + 20 (0.637)
        },

        {
            "name": "East End Eatery",
            "googleRating": 4.6,        
            "googleReviews": 422,
            "redditMentions": 2,
            "averageUpvotes": 12.5,
            "sentimentScore": 1.000,  
        },
        
        {
            "name": "Country Foodly",
            "googleRating": 4.6,        
            "googleReviews": 776,
            "redditMentions": 2,
            "averageUpvotes": 51.0,
            "sentimentScore": 0.904,    # avg of comments 9 (1.000) + 14 (0.807)
        },

        {
            "name": "Seoul Pocha",
            "googleRating": 4.7,        
            "googleReviews": 423,
            "redditMentions": 2,
            "averageUpvotes": 18.5,
            "sentimentScore": 0.000,    # avg of comments 15 (0.000) + 21 (0.000)
        },
        {
            "name": "WaHaHa",
            "googleRating": 4.4,        
            "googleReviews": 852,
            "redditMentions": 2,
            "averageUpvotes": 11.0,
            "sentimentScore": 0.784,    
        },

        {
            "name": "La Cocina de Abuela",
            "googleRating": 4.6,
            "googleReviews": 768,
            "redditMentions": 2,
            "averageUpvotes": 16.5,
            "sentimentScore": 0.423,    # avg of comments 28 (0.273) + 41 (0.572)
        },

        {
            "name": "Tup Tim Thai",
            "googleRating": 4.2,        
            "googleReviews": 493,
            "redditMentions": 1,
            "averageUpvotes": 24.0,
            "sentimentScore": 0.000,  
        },

        {
            "name": "Zeezenia",
            "googleRating": 4.6,        
            "googleReviews": 729,
            "redditMentions": 1,
            "averageUpvotes": 20.0,
            "sentimentScore": 1.000,   
        },

        {
            "name": "43rd Street Deli",
            "googleRating": 4.5,        
            "googleReviews": 1023,
            "redditMentions": 1,
            "averageUpvotes": 20.0,
            "sentimentScore": 1.000,   
        },

        {
            "name": "Indian Cuisine",
            "googleRating": 4.2,        
            "googleReviews": 943,
            "redditMentions": 1,
            "averageUpvotes": 20.0,
            "sentimentScore": 1.000,    
        },

        {
            "name": "Indian Aroma",
            "googleRating": 4.7,        
            "googleReviews": 291,
            "redditMentions": 1,
            "averageUpvotes": 39.0,
            "sentimentScore": 0.647,   
        },
        {
            "name": "Hogan's",
            "googleRating": 4.6,        
            "googleReviews": 1575,
            "redditMentions": 1,
            "averageUpvotes": 20.0,
            "sentimentScore": 0.710,    
        },

        {
            "name": "Di Big Jerk",
            "googleRating": 4.3,
            "googleReviews": 146,
            "redditMentions": 1,
            "averageUpvotes": 59.0,
            "sentimentScore": 0.994,   
        },
    
        {
            "name": "Adam's Rib",
            "googleRating": 4.5,
            "googleReviews": 2033,
            "redditMentions": 1,
            "averageUpvotes": 2.0,
            "sentimentScore": 0.836,   
        },
        {
            "name": "La Tienda",
            "googleRating": 4.5,
            "googleReviews": 2952,
            "redditMentions": 1,
            "averageUpvotes": 2.0,
            "sentimentScore": 0.836,  
        },
        
        {
            "name": "Square House Pizza",
            "googleRating": 4.6,        
            "googleReviews": 624,
            "redditMentions": 1,
            "averageUpvotes": 39.0,
            "sentimentScore": 0.000,  
        },

        {
            "name": "M&D West African Cuisine",
            "googleRating": 4.9,
            "googleReviews": 195,
            "redditMentions": 1,
            "averageUpvotes": 8.0,
            "sentimentScore": 0.885,   
        }
    ]

    ranked = scoreDestinations(testDestinations)

    print("=== Project Paraíba — Hidden Gem Rankings ===")
    print(f"Weights = Reddit: {redditWeight}  |  ML: {mlWeight}  |  Google: {googleWeight}\n")
    for i, dest in enumerate(ranked, 1):
        r = dest["Score Result"]
        print(f"{i}. {dest['name']}")
        print(f"   Score:   {r['Paraíba Score']} / 100")
        print(f"   Reddit: {r['Reddit Score']}  |  ML: {r['ML Score']}  |  Google: {r['Google Score']}\n")

    print("\n=== Ranked by Reddit Score ===\n")
    reddit_ranked = sorted(ranked, key=lambda x: x["Score Result"]["Reddit Score"], reverse=True)
    for i, dest in enumerate(reddit_ranked, 1):
        print(f"{i}. {dest['name']:<30} Reddit: {dest['Score Result']['Reddit Score']}")

    print("\n=== Ranked by ML Score (Sentiment) ===\n")
    ml_ranked = sorted(ranked, key=lambda x: x["Score Result"]["ML Score"], reverse=True)
    for i, dest in enumerate(ml_ranked, 1):
        print(f"{i}. {dest['name']:<30} ML: {dest['Score Result']['ML Score']}")

    print("\n=== Ranked by Google Score ===\n")
    google_ranked = sorted(ranked, key=lambda x: x["Score Result"]["Google Score"], reverse=True)
    for i, dest in enumerate(google_ranked, 1):
        print(f"{i}. {dest['name']:<30} Google: {dest['Score Result']['Google Score']}")
