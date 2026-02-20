import requests
from geopy.geocoders import Nominatim #add to dependancies
from typing import List


class GooglePlacesValidator:
    #this class is to validate the entity names from spaCy and get the name, location, category, # of reviews, and rating from Google 
    
    def __init__(self, api_key: str, default_location: str = "Gainesville, FL", radius: int = 25000):
        #set default location to gainesville 
        self.api_key = api_key
        self.default_location = default_location
        self.radius = radius
        self.api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json" #set the api call to get the name from text
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json" #set the api call to get details from the resulting place ID
        self.geocoder = Nominatim(user_agent ="ParaibaModel") #get the imported class
        self.cordsCache = {} #store a cache for locations

    def _get_coordinates(self, location: str): #get the coordinates for a location
        if location in self.cordsCache: #if the location is in the cache
            return self.cordsCache[location] #return the coordinates
        try:
            getLoc = self.geocoder.geocode(location) #geocode the location according to geopy
            if getLoc: #if it gets coordinates
                coords = (getLoc.latitude, getLoc.longitude) #then coordinates are (lat, long)
                self.cordsCache[location]=coords #store it in the cache
                return coords #return the coordinates
            else:
                print(f"Could not find coordinates for '{location}'") #else print error
                return None #return no coordinates
        except Exception as e:
            print(f"Geocoding error: {e}") #pring if error
            return None
        
    def validate_loc(self, entity: str, location: str = None):
        #this function returns a dictionary of the name, address, rating, number of reviews, category, and place id for a single location
        
        if location is None: #do not search without location
            location = self.default_location
        
        # Build search query with full venue name
        search_query = f"{entity} near {location}"

        coords = self._get_coordinates(location)
        
        # API parameters
        findID = {
            'input': search_query, #entity name and location given
            'inputtype': 'textquery', #input of text
            'fields': 'place_id', #Get the place ID to make another API call to find the details needed
            'key': self.api_key 
        }

        if coords:
            lat, lon = coords
            findID['locationbias'] = f'circle:{self.radius}@{lat}, {lon}'
            print(f"Searching: {search_query} (within {self.radius/1609:.1f} miles)")
        else:
            print(f"Searching: {search_query} (no location radius)")
        try:
            # Make API request
            response = requests.get(self.api_url, params=findID)
            data = response.json()

            print(f"\n {search_query}'")
            print(f"Restuarant info: {data}")
            
            if data.get('status') != 'OK' or not data.get('candidates'): #if the status is not 'OK' and does not return a set of locations

                print(f"Not found")

                return None 
            placeID = data['candidates'][0].get('place_id') #add id to list
            if not placeID:

                print(f"No place_id returned")

                return None #if it cant get placeID then dont return
                              
            detailsParams = {
                'place_id': placeID,
                'fields': 'name,formatted_address,rating,user_ratings_total,types,editorial_summary,reviews', #get the name, address, rating, total reviews, category, 
                #description, and top 5 reviews
                'key': self.api_key
            }


            finalResponse = requests.get(self.details_url, params=detailsParams) #call the api again to get all the details required
            finalData = finalResponse.json() #write it as json

            #below is to ensure the places match
            place = finalData.get('result', {}) #get the name from final result
            place_name = place.get('name', '') #get the name from original text
            entity_lower = entity.lower() #get both to lower to ensure that characters match
            place_lower = place_name.lower()
            entity_words = set(entity_lower.replace("'s", "").split()) #just incase there are apostrophes
            place_words = set(place_lower.replace("'s", "").split())
            overlap = len(entity_words & place_words) #get how many characters match each other
            match_ratio = overlap / len(entity_words) if entity_words else 0 #if the overlap is less than 50% of the words

            if match_ratio < 0.5: #if less than 0 dont return

                print(f"google and spacy does not match")

                return None

            if finalData.get('status') != 'OK':

                print(f"Could not get details")

                return None #returns none if the details were not fetched
            
            place = finalData.get('result', {}) #get the object
            summary = place.get('editorial_summary', {})
            description = summary.get('overview') if summary else None #gets the description if it is available as overview otherwise dont return
            reviews = place.get('reviews', [])
            topReviews = []
            for review in reviews[:5]:
                topReviews.append({
                    'text': review.get('text')
                })  

            return{
                'name': place.get('name'), #get the name of the place
                'address': place.get('formatted_address'), #get the address
                'rating': place.get('rating', 'N/A'), #get the rating
                'review_count': place.get('user_ratings_total', 0), #get the number of reviews
                'category': place.get('types'), #get the category
                'description': description, #get the description
                'googlereviews': topReviews #get the top 5 reviews
            }
            
        except Exception as e:
            print(f"   Error validating {entity}: {e}") #print the entity name and error if something goes wrong
            return None
    def validate_all_locs(self, entities: List[str]): #this function validates all locations given in a list, what we need
        validatedEntities = [] #list of validated locations
        for entity in entities:
            checkEntity = self.validate_loc(entity) #run validate location on every entity in list given

            if checkEntity:
                validatedEntities.append(checkEntity) #if google finds it add it in

                print(f"✓ {checkEntity['name']} - {checkEntity['rating']}/5")

            else:
                print(f"Location: {checkEntity} was not found by Google /n") #if not then print this error message

                print(f"✗ {entity} was not found by Google")

        return validatedEntities

def google_full(entities: List[str], apiKey: str, location: str = "Gainesville, FL", radius: int = 25000): #callable function to run entire class
    validator = GooglePlacesValidator(apiKey, location, radius)
    return validator.validate_all_locs(entities)