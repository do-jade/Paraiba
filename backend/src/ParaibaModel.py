from spaCyNER import spaCy_full
from PlacesAPI import google_full
from pymongo import MongoClient
from dotenv import load_dotenv
from vader import analyzer 
from rankingModel import paraibaScore
import re
import os

#reminder that it must run py -3.12 -m pip install ...

# Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') #Google API key from .env
MONGO_URI = os.getenv("MONGODB_CONNECTION") #MongoDB connection string from .env

# Connect to MongoDB
client = MongoClient(MONGO_URI) #open client from connection string
db = client["test"] # the database that houses the info is in test
redditCollection = db["comments"] #this is where the unprocessed, scraped Reddit API data is
paraibaCollection = db["paraibas"] #this collection is where the info from this file will go

TEST = False
if TEST:
    # Test with hardcoded data
    comments = [
        {
            '_id': '6993f3b8dedc9dd1aac4e9f7',
            'comment_text': "A little outside the city but Pearl's. It’s attached to a gas station/convenience store but it is unbelievable. Definitely worth the drive and certainly underrated.",
            'upvotes': 47,
            'link': 'https://www.reddit.com/r/GNV/comments/dydpd0/whats_the_most_underrated_restaurant_in_town/f80i6es',
            'processed': False
        }
    ]
    print("TEST")
else:
    comments = list(redditCollection.find({'$or': [{'processed' :{'$ne': True}}, {'processed': {'$exists': False}}]})) #Gets all comments to go through them, this is for all in mongo

totLocations = paraibaCollection.find({}, {'name':1}) #get name field
existingLocations = {} #dictionary with lowercase names
for loc in totLocations: #for every location in the list
    locName = loc['name'].lower() #get the name lowercase to ensure that every name is the same
    existingLocations[locName] = {
        'name': loc['name'],
        '_id': loc['_id']
    } #add the location data from collection to that name 

placeCategories = { #matches on these keywords to check for a category manualy, google does not do a good job at this
    # Cuisine indicators, can add more latter
    "american": ["american", "southern", "soul food", "comfort food", "cajun", "creole"],
    "bbq": ["bbq", "barbecue", "barbeque", "smokehouse", "smoked", "brisket", "ribs"],
    "caribbean": ["caribbean", "jamaican", "jerk", "haitian", "trinidadian", "cuban", "plantain"],
    "chinese": ["chinese", "dim sum", "cantonese", "szechuan", "hunan", "hong kong"],
    "italian": ["italian", "pizza", "pasta", "trattoria", "osteria", "risotto", "gelato"],
    "japanese": ["japanese", "sushi", "ramen", "izakaya", "tempura", "udon", "soba", "omakase"],
    "korean": ["korean", "kbbq", "korean bbq", "bibimbap", "bulgogi", "tteokbokki"],
    "mexican": ["mexican", "tex-mex", "tacos", "burrito", "enchilada", "tamale", "taqueria"],
    "mediterranean": ["mediterranean", "greek", "turkish", "lebanese", "persian", "falafel", "hummus", "shawarma"],
    "indian": ["indian", "tandoori", "biryani", "naan", "dosa", "chai"],
    "vietnamese": ["vietnamese", "pho", "banh mi", "spring rolls", "bun bo hue"],
    "thai": ["thai", "pad thai", "green curry", "tom yum", "satay"],
    "seafood": ["seafood", "fish", "shrimp", "crab", "lobster", "oyster", "clam", "boil"],
    "steakhouse": ["steakhouse", "steak", "steaks", "chophouse", "sirloin", "ribeye"],
    "burgers": ["burger", "burgers", "smash burger", "cheeseburger"],
    "sandwiches": ["sandwich", "sandwiches", "sub", "hoagie", "cheesesteak", "deli"],
    "bakery": ["bakery", "pastry", "croissant", "bagel", "bagels", "donuts", "bread"],
    "cafe": ["cafe", "café", "coffee", "espresso", "latte", "brunch", "breakfast"],
    "dessert": ["ice cream", "gelato", "frozen yogurt", "dessert", "sweets", "chocolate"],
    "brewery": ["brewery", "brewpub", "craft beer", "taproom", "ales", "lager"],
    "winery": ["winery", "wine bar", "wine", "vineyard", "tasting room"],
    "bar": ["bar", "lounge", "cocktail", "speakeasy", "pub", "tavern"],

    # Outdoor and nature categories, can add more later
    "hiking": ["hiking", "hike", "trail", "trails", "trailhead", "backpacking", "trekking"],
    "park": ["park", "preserve", "greenway", "recreation area", "national park", "state park"],
    "water sports": ["kayak", "canoe", "paddleboard", "paddle board", "rowing", "tubing", "rafting"],
    "swimming": ["swimming", "swim", "pool", "splash pad", "springs", "swimming hole"],
    "cycling": ["cycling", "biking", "bike trail", "mountain bike", "bmx"],
    "camping": ["camping", "campground", "campsite", "glamping", "rv park"],
    "wildlife": ["wildlife", "birds", "birdwatching", "birding", "gators", "deer", "nature walk"],
    "water body": ["lake", "river", "creek", "pond", "wetlands", "marsh", "spring", "beach"],

    # Accessibility
    "wheelchair accessible": ["wheelchair", "accessible", "ada", "handicap", "mobility", "paved trail", "flat trail"],

    # Arts and Entertainment
    "museum": ["museum", "history", "science center", "exhibit", "gallery", "art museum"],
    "performing arts": ["theater", "theatre", "cinema", "movie", "comedy", "live music", "concert", "opera"],
    "arcade": ["arcade", "bowling", "mini golf", "go kart", "axe throwing", "escape room"],

    # Fitness
    "fitness": ["gym", "fitness", "yoga", "pilates", "crossfit", "weightlifting", "rock climbing", "skatepark"],

    # Shopping & Markets
    "market": ["market", "farmer's market", "farmers market", "food hall", "food truck", "pop up"],
}

def getCategory(name, description, reviews, googleTypes): #look at name, description, review, and google types to see if it can match a category
    def wordMatch(keyword, text): #function to match on words using regex, keyword must be a standalone word
        return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text))
    
    def reviewMatchCount(keyword, reviewList): #loops through every review and counts how many individual reviews have the keyword associated with it
        return sum(1 for r in reviewList if wordMatch(keyword, r.get('text', '').lower())) #helps to cut down on extra categories
    
    primaryText = " ".join([name or "", description or "", " ".join(googleTypes or [])]).lower() #combine name, description, and tags to see if a category matches
    googleTypesLower = [t.lower() for t in (googleTypes or [])]
    googleTypeMap = { "bar": "bar", "cafe": "cafe", "museum": "museum", "park": "park", "campground": "camping", "gym": "fitness", "stadium": "performing arts", "movie_theater": "performing arts", "bowling_alley": "arcade", "zoo": "wildlife", "aquarium": "wildlife",}
    found = [] #above is to match on googles categories, does not really help tho
    for gType, mappedCategory in googleTypeMap.items(): #if it does match then append onto category
        if gType in googleTypesLower and mappedCategory:
            found.append(mappedCategory) 
    outdoorOnlyCategories = {"hiking", "park", "water sports", "swimming", "cycling", "camping", "wildlife", "water body"} #outdoor only to help with distinction between indoor and outdoor
    reviewThreshold = 1 if len(reviews) <=3 else 2 #if the number of reviews is less than 3 then one review can count for category, otherwise 2 reviews must share same keyword

    for category, keywords in placeCategories.items(): #run through every category and match based on confidence
        if category in found: #if already part of category stkip
            continue
        if any(wordMatch(kw, primaryText) for kw in keywords):
            found.append(category) #if the name, description, and type match append the category
            continue
        if category in outdoorOnlyCategories: #dont check reviews for these as people can put in random keywords that will hit, dont want a trail to include a bar bc someone drank a beer on it
            continue
        reviewVotes = sum( 1 for kw in keywords if reviewMatchCount(kw, reviews) >= reviewThreshold)
        if reviewVotes >= 1: #counts how many keywords appear and if they have a good reviewcount then add the category in
            found.append(category) #this helps from a random trail having 12 categories including restuarants
    found = list(dict.fromkeys(found)) #deduplicate the list to make sure the same category does not appear more than once

    outdoorCategories = {"hiking", "park", "water sports", "swimming", "cycling", "camping", "wildlife", "water body"} #categories from above that match outdoors
    indoorCategories = {"museum", "performing arts", "arcade", "fitness", "bakery", "cafe", "brewery", "winery", "bar"} #categories from above that match indoors

    outdoorKeywords = ["outside", "outdoor", "open air", "open-air", "patio", "rooftop"] #additional outdoor keywords that may represent it better
    indoorKeywords = ["inside", "indoor", "air conditioned", "air-conditioned", "cozy", "intimate"] #additional indoor keywords that may represent it better

    isOutdoor = (
        any(cat in found for cat in outdoorCategories) or
        any(wordMatch(kw, primaryText) for kw in outdoorKeywords)
    )
    isIndoor = (
        any(cat in found for cat in indoorCategories) or
        any(wordMatch(kw, primaryText) for kw in indoorKeywords)
    )

    if isOutdoor and isIndoor:
        found.append("indoor/outdoor")  #indoor/outdoor has both  then add
    elif isOutdoor:
        found.append("outdoor") #only outdoors then add
    elif isIndoor:
        found.append("indoor") #only indoors then add

    return found if found else ["general"] #if none matches then it gets put in general category

def matchLocs(spaCy, existing): #this is a helper function to match spacy names to place API names 
    cleaned = spaCy.lower() #get spacy extracted name in lowercase
    if cleaned in existing: #if it is an exact match
        return (cleaned, existing[cleaned]) #return it
    
    spacy_words = set(cleaned.replace("'s", "").replace("'s", "").split()) #fixing for apostrophes again :(

    for gName, details in existing.items(): #check for substring match
        dWords = set(gName.replace("'s", "").replace("'s", "").split()) #do the same apostrophe checking 
        overlap = len(spacy_words & dWords) #get the word length together
        if overlap >=1: #if at least one word matches
            return(gName, details) #return it
    
    return (None, None) #cannot find it

allLocations = {}  #List to get all comment's locations

for i, comment in enumerate(comments, 1): #for every comment 
    commentText = comment['comment_text'] #store the comment
    upvotes = comment['upvotes'] #store the upvotes
    link = comment['link'] #store the link
    #above is to be used later to put into paraibas collection
    
    spaCyEntities = spaCy_full(commentText) #extract the name(s) with spacy
    for loc in spaCyEntities: #had to change from i to loc: overwritten i a couple of times
        print(f"Locs found: {loc}")
    
    if not spaCyEntities: #if not in the spaCyEntities list then continue
        continue

    # Group comments by location
    for locName in spaCyEntities: #This allows to check multiple entities within a single comment
        matchedName, matchedLocation = matchLocs(locName, existingLocations) #get the name and location from the matching function
        # Use matched key if found, otherwise use normalized name
        if matchedName: #if it finds a matched name then use it
            cleanedLocName = matchedName
        else:
            cleanedLocName = locName.lower() #else use the lowered name

        if cleanedLocName not in allLocations: #if it is not in all locations then add it
            allLocations[cleanedLocName] = {
                'name': locName,
                'comments': []
            }

        allLocations[cleanedLocName]['comments'].append({ #if the location exists then add the comments, upvotes, and link
            'text': commentText,
            'upvotes': upvotes,
            'link': link
        }) 

    redditCollection.update_one( #issue with comments duplicating, so update the reddit comments here
        {'_id': comment['_id']},
        {'$set': {'processed': True}}
    )     

# Separate new vs existing locations
newLocations = [name for cleanName, name in allLocations.items() if cleanName not in existingLocations] #if the name is in the total locations and not in paraibas collection then add to newLocations
updateTheLocs = [(cleanName, info) for cleanName, info in allLocations.items() if cleanName in existingLocations] #if the name is in total Locations and in the paraibas collection then need to update it

print(f"{len(newLocations)} new locations")
print(f"{len(updateTheLocs)} existing locations to update")

currentLocation = "Gainesville, FL" #static location for now, but can update it later
calledGoogle = [] #hold locations called by Places API
if newLocations:  # if the name is new to the pariabas collection

    nameValidation = [info['name'] for info in newLocations] #for every name in the new location
    calledGoogle = google_full(nameValidation, GOOGLE_API_KEY, currentLocation) #call the places api to get the google information
    #this duplication check allows for names to only be called when new
    for gLoc in calledGoogle: #for every location in the places API calls
        # Find matching venue data
        matching = None
        for loc in newLocations: #if names match correctly then go forward with it
            if loc['name'].lower() == gLoc['name'].lower():
                matching = loc
                print("names match exactly")
                break
        if not matching: 
            for loc in newLocations:
                spacy_words = set(loc['name'].lower().replace("'s", "").replace("'s", "").split()) #ensure apostrophes match between the two
                google_words = set(gLoc['name'].lower().replace("'s", "").replace("'s", "").split())
                

                overlap = len(spacy_words & google_words)
                iFpossessive = loc['name'].endswith("'s") or loc['name'].endswith("\u2019s")
                if (iFpossessive and overlap >= 1) or overlap >= 2: #if at least 2 words match or is a possesive name
                    matching = loc
                    print("went for the overlap")
                    break
        if matching:
            commentTexts = [comment['text'] for comment in matching['comments']] #aggreagate all matching comments for one location
            sentimentFull = analyzer(commentTexts) #get all three results from vader   
            totalUpVote = sum(comment['upvotes'] for comment in matching['comments']) #get total upvotes
            avgUpVote = totalUpVote/len(matching['comments']) #average it

            rankingResult = paraibaScore( #get paraibaScore
                googleRating=gLoc['rating'] if isinstance(gLoc['rating'], (int, float)) else 0, #get rating
                googleReviews=gLoc['review_count'], #get reviewCount
                redditMentions=len(matching['comments']), #get current number of mentions
                averageUpvotes=avgUpVote, #get average up vote
                sentimentScore=sentimentFull['compound'] if sentimentFull else 0 #get vader sentiment
            )

            categoryType = getCategory(
                gLoc['name'], gLoc.get('description'), gLoc.get('googlereviews', []), gLoc.get('category', []) #run get cuisine to get the cuisine, if it does not find one it is general
            )
 
            paraibaCollection.update_one( #Changed from Insert to update to ensure duplicates are handled
                {'name': gLoc['name']}, #name from places API, matches on the name
                {'$setOnInsert': { #sets on insert if the document is being inserted for the first time
                    'address': gLoc['address'], #address from places API
                    'category': gLoc['category'], #category from places API
                    'reviewCount': gLoc['review_count'], #review count from places API
                    'rating': gLoc['rating'], #rating from places API
                    'description': gLoc.get('description'), #description from places API
                    'sentimentRating': sentimentFull['compound'] if sentimentFull else None, #This is a call from VADER and gets the compound number
                    'ranking': rankingResult['Paraíba Score'], #This is a call from ranking model
                    'upvotes': sum(comment['upvotes'] for comment in matching['comments']), #upvotes from comments collection
                    'mentionCount': len(matching['comments']), #This currently is not in the collection
                    'location': currentLocation, #this comes from description inputted into Places API, not in collection
                    'comments': [{'text': c['text']} for c in matching['comments']], #comments from comments collection, gets only the text from above
                    'googleReviews': gLoc.get('googlereviews', []), #reviews are comments from places API
                    'link': [comment['link'] for comment in matching['comments']], #link from comments collection and returns all associated links
                    'categoryType': categoryType, #get category
                    'servesBreakfast': gLoc.get('serves_breakfast', False), #google has the ones below
                    'servesBrunch': gLoc.get('serves_brunch', False), #All these do are return true or false
                    'servesLunch': gLoc.get('serves_lunch', False),
                    'servesDinner': gLoc.get('serves_dinner', False),
                    'servesBeer': gLoc.get('serves_beer', False),
                    'servesWine': gLoc.get('serves_wine', False),
                    'servesVegetarian': gLoc.get('serves_vegetarian', False),
                    'dineIn': gLoc.get('dine_in', False),
                    'takeout': gLoc.get('takeout', False),
                    'delivery': gLoc.get('delivery', False),
                 }},
                upsert=True #protect against duplicates
            ) 
        else:
            print(f"No match found for {gLoc['name']}")

#check for reddit comments are the same            

# Update existing venues with new comments
if updateTheLocs:   

    print(f"\nUpdating {len(updateTheLocs)} existing locations...")

    for uLoc, locInfo in updateTheLocs: #for every name that is already in Paraibas collection
        if uLoc not in existingLocations:
            print(f"Warning: {locInfo['name']} not in existing locations")
            continue #if it is not in the existing locations dont even try
        exisitingLocInfo = existingLocations[uLoc] #get info from existing location
        newComments = locInfo['comments'] #get new comments
        totalMentions = exisitingLocInfo.get('mentionCount', 0) + len(newComments) #get total mentions of the location
        totUpvotes = sum(comments['upvotes'] for comments in newComments) #get total upvotes from all comments about one location
        avgUpvotes = totUpvotes / totalMentions #get average up votes

        findOldComms = paraibaCollection.find_one({'_id': exisitingLocInfo['_id']}) #find the location using mongo's id
        
        getAllComments = [comment['text'] for comment in findOldComms.get('comments', [])] # get all existing comments at the mongo ID

        getAllComments.extend([comment['text'] for comment in newComments]) #add the new comments to the old ones
        sentimentScore = analyzer(getAllComments) #get vader score of all associated comments

        rankingResult = paraibaScore( #same as above
            googleRating=exisitingLocInfo.get('rating', 0) if isinstance(exisitingLocInfo.get('rating'), (int, float)) else 0, #get rating
            googleReviews=exisitingLocInfo.get('reviewCount', 0), #get reviews
            redditMentions=totalMentions, #get mentions
            averageUpvotes=avgUpvotes, #get average up votes
            sentimentScore=sentimentScore['compound'] if sentimentScore else 0 #get current sentiment score
        )
        
        sentimentScore = analyzer(getAllComments) #get vader score of all associated comments
        paraibaCollection.update_one(
            {'_id': exisitingLocInfo['_id']}, #for the id mentioned
            {
                '$inc': {'upvotes': totUpvotes, 'mentionCount': len(newComments)}, #put in total upvotes and mention count which is the number of comments that mention it
                '$push': {'comments': {'$each': newComments}}, #append the new comments
                '$set': {'sentimentRating': sentimentScore['compound'], 'ranking': rankingResult['Paraíba Score'] } #set the new vader score in place of the old one as well as paraiba
            }
        )
        #got rid of updatin the processed flag as true here and moved it up

client.close() #close mongo