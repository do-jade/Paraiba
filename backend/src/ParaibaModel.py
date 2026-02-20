from spaCyNER import spaCy_full
from PlacesAPI import google_full
from pymongo import MongoClient
from dotenv import load_dotenv
from vader import analyzer 
from rankingModel import paraibaScore
import os

# Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') #Google API key from .env
MONGO_URI = os.getenv("MONGODB_CONNECTION") #MongoDB connection string from .env

# Connect to MongoDB
client = MongoClient(MONGO_URI) #open client from connection string
db = client["test"] # the database that houses the info is in test
redditCollection = db["comments"] #this is where the unprocessed, scraped Reddit API data is
paraibaCollection = db["paraibas"] #this collection is where the info from this file will go

TEST = True
if TEST:
    # Test with hardcoded data
    comments = [
        {
            '_id': '6993f3b8dedc9dd1aac4e9f2',
            'comment_text': "A little outside the city but Pearl’s Country Store and BBQ is incredible. It’s attached to a gas station/convenience store but it is unbelievable. Definitely worth the drive and certainly underrated.",
            'upvotes': 47,
            'link': 'https://www.reddit.com/r/GNV/comments/dydpd0/whats_the_most_underrated_restaurant_in_town/f80i6es',
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

def matchLocs(spaCy, existing): #this is a helper function to match spacy names to place API names 
    cleaned = spaCy.lower() #get spacy extracted name in lowercase
    if cleaned in existing: #if it is an exact match
        return (cleaned, existing[cleaned]) #return it
    
    spacy_words = set(cleaned.replace("'s", "").replace("'s", "").split()) #fixing for apostrophes again :(

    for gName, details in existing.items(): #check for substring match
        dWords = set(gName.replace("'s", "").replace("'s", "").split()) #do the same apostrophe checking 
        overlap = len(spacy_words & dWords) #get the word length together
        if overlap >=2: #if more than two words match
            return(gName, details) #return it
    
    return (None, None) #cannot find it

allLocations = {}  #List to get all comment's locations

for i, comment in enumerate(comments, 1): #for every comment 
    commentText = comment['comment_text'] #store the comment
    upvotes = comment['upvotes'] #store the upvotes
    link = comment['link'] #store the link
    #above is to be used later to put into paraibas collection
    
    spaCyEntities = spaCy_full(commentText) #extract the name(s) with spacy
    for i in spaCyEntities:
        print(f"Locs found: {i}")
    
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
                if overlap >= 2: #if at least 2 words match
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
 
            paraibaCollection.insert_one({
                'name': gLoc['name'], #name from places API
                'address': gLoc['address'], #address from places API
                'category': gLoc['category'], #category from places API
                'reviewCount': gLoc['review_count'], #review count from places API
                'rating': gLoc['rating'], #rating from places API
                'description': gLoc.get('description'), #description from places API
                'sentimentrating': sentimentFull['compound'] if sentimentFull else None, #This is a call from VADER and gets the compound number
                'ranking': rankingResult['Paraíba Score'], #This is a call from ranking model
                'upvotes': sum(comment['upvotes'] for comment in matching['comments']), #upvotes from comments collection
                'mentionCount': len(matching['comments']), #This currently is not in the collection
                'location': currentLocation, #this comes from description inputted into Places API, not in collection
                'comments': [{'text': c['text']} for c in matching['comments']], #comments from comments collection, gets only the text from above
                'googleReviews': gLoc.get('googlereviews', []), #reviews are comments from places API
                'link': [comment['link'] for comment in matching['comments']], #link from comments collection and returns all associated links
            }) 
        else:
            print(f"No match found for {gLoc['name']}")

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
                '$set': {'sentimentrating': sentimentScore['compound'], 'ranking': rankingResult['Paraíba Score'] } #set the new vader score in place of the old one as well as paraiba
            }
        )
        redditCollection.update_one( #this updates the comment to flag it to be true
            {'_id': comment['_id']},
            {'$set': {'processed': True}}
        )

client.close() #close mongo
