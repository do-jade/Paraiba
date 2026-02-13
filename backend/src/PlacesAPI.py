import requests
from typing import List


class GooglePlacesValidator:
    #this class is to validate the entity names from spaCy and get the name, location, category, # of reviews, and rating from Google 
    
    def __init__(self, api_key: str, default_location: str = "Gainesville, FL"):
        #set default location to gainesville 
        self.api_key = api_key
        self.default_location = default_location
        self.api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json" #set the api call
        
    def validate_loc(self, entity: str, location: str = None):
        #this function returns a dictionary of the name, address, rating, number of reviews, category, and place id for a single location
        
        if location is None: #do not search without location
            location = self.default_location
        
        # Build search query with full venue name
        search_query = f"{entity} {location}"
        
        # API parameters
        params = {
            'input': search_query, #entity name and location given
            'inputtype': 'textquery', #input of text
            'fields': 'name,formatted_address,rating,user_ratings_total,place_id,types', #these are the returnned variables we want
            'key': self.api_key 
        }
        
        try:
            # Make API request
            response = requests.get(self.api_url, params=params)
            data = response.json()

            print(f"\n {search_query}'")
            print(f"Restuarant info: {data}")
            
            if data.get('status') == 'OK' and data.get('candidates'): #if the status is 'OK' and returns a set of locations
                place = data['candidates'][0] #add locations to list
                              
                #then return the information held in place
                return {
                    'name': place.get('name'),
                    'address': place.get('formatted_address'),
                    'rating': place.get('rating', 'N/A'),
                    'review_count': place.get('user_ratings_total', 0),
                    'place_id': place.get('place_id'),
                    'category': place.get('types')
                }
            
            return None #if status is not ok 
            
        except Exception as e:
            print(f"   Error validating {entity}: {e}") #print the entity name and error if something goes wrong
            return None
    def validate_all_locs(self, entities: List[str]): #this function validates all locations given in a list, what we need
        validatedEntities = [] #list of validated locations
        for entity in entities:
            checkEntity = self.validate_loc(entity) #run validate location on every entity in list given

            if checkEntity:
                validatedEntities.append(checkEntity) #if google finds it add it in

            else:
                print(f"Location: {checkEntity} was not found by Google /n") #if not then print this error message
        return validatedEntities

def google_full(entities: List[str], apiKey: str, location: str = "Gainesville, FL"): #callable function to run entire class
    validator = GooglePlacesValidator(apiKey, location)
    return validator.validate_all_locs(entities)