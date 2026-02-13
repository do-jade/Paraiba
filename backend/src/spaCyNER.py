# python -m spacy download en_core_web_lg

import re #regex for cleaning up entities
import spacy #import spacy NER
class spaCyEntities:
    def __init__(self):
        self.nlp = self._build_nlp() #initialize nlp with custom patterns below

    def _build_nlp(self): #set the patterns and build nlp pipeline
        nlp = spacy.load("en_core_web_lg") #load the pre-trained large English semantic model
        ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True}) #entity ruler allows for custom patterns to be used
        #the patterns are ran before the natural entity processing spaCy does and the patterns will overwrite what spaCy gives
        #basically want to ensure that all locations and restuarants are labeled as places to be picked up later

        patterns = [ #custom patterns created specifically to pick up restuarants and attractions
            # This is to pick up names with 2 capitalized letters and a description about it EX: Hana Sushi grill picks up the first two as well as grill in list
            #This will not pick up Sushi Grill as Grill is a suffix, may have to fix later
            {"label": "PLACE", "pattern": [ #label is set to PLACE for pick up later
                {"IS_TITLE": True}, #picks the first captitalized word
                {"IS_TITLE": True, "OP": "+"}, #OP + is get at least 2 captitalized words
                {"LOWER": {"IN": ["grill","bbq","kitchen","market","deli","cafe","café"]}} #need to make this longer to accept more
            ]},

            # This pattern is to pick up verbs people would place infront of a place
            {"label": "PLACE", "pattern": [
                {"LOWER": {"IN": ["try","visit","visited","loved","love","ate","dined", "be", "liked", "and", "or"]}}, #trigger the match like "loved Satchel's", however wont pick up ate yesterday 
                {"IS_TITLE": True, "OP": "+"} #grabs the title
            ]},

            # Continues the trigger word but adds the two in for go and went Ex went to Marks
            {"label": "PLACE", "pattern": [
                {"LOWER": {"IN": ["go","went"]}}, #if the sentence has go or went
                {"LOWER": "to"}, #and the next word is to
                {"IS_TITLE": True, "OP": "+"} #then grab the title of the restuarant and other titles capitalized afterwards
                #I need to create more lowercase patterns 
            ]},

            # pattern matches titles after the word at Ex at El Indio
            {"label": "PLACE", "pattern": [
                {"LOWER": "at"}, #is at is before titel
                {"IS_TITLE": True, "OP": "+"} #grab the title and any others after it
            ]},

            # pattern matches describing the food category with a semicolon and picks up the title and other capitalized words after EX thai: Green Papaya
            #This was a common listing method in some subreddits, more of an edge case
            {"label": "PLACE", "pattern": [
                {"LOWER": {"IN": ["thai","pho","jamaican","chinese","burger","bread","mexican","southern","sandwiches","gyro"]}}, #
                {"TEXT": ":"},
                {"IS_TITLE": True},
                {"IS_TITLE": True, "OP": "?"},
                {"IS_TITLE": True, "OP": "?"},
                {"IS_TITLE": True, "OP": "?"},
            ]},

            #pattern matches a title and extra titles before the words has, is, was again another edge case EX Paper Bag Deli is ...
            {"label": "PLACE", "pattern": [
                {"IS_TITLE": True, "OP": "+"},
                {"LOWER": {"IN": ["has","is","was"]}}
            ]},

            # pattern matches for apostrophes EX DJ's, this may need to be tweaked also grabs words after
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": r"^[A-Z][A-Za-z]{1,}('s| 's)?$"}}, #this regex is to get a capital letter then accept any letter with a name greater than 1 char and has 's
                {"TEXT": {"IN": ["'s", "'s"]}},
                {"TEXT": {"REGEX": r"^([A-Z][a-z]+|grill|bbq|kitchen|market|deli|cafe|café|pizza|burgers)$"}, "OP": "*"} #this grabs any title case after OR any lowercase common places
            ]},

            {"label": "PLACE", "pattern": [ #for possesive names only
                {"TEXT": {"REGEX": r"^[A-Z][A-Za-z]{1,}$"}},  # Capitalized word
                {"TEXT": {"IN": ["'s", "'s"]}}  # Followed by 's
            ]},
            
            {"label": "PLACE", "pattern": [
                {"TEXT": {"IN": [","]}},
                {"IS_TITLE": True, "OP": "+"} #This gets lists 
            ]},

            #There are more patterns to add to get more generalized entity rulings
        ]

        ruler.add_patterns(patterns) #load all patterns to entity ruler
        return nlp #return the nlp object with custom patterns added in

    def _clean_entity(self, text: str): #cleans up the entities and returns a string
        text = text.replace("'", "'").replace(""",'"').replace(""", '"') #This gets rid of extra quotes
        text = re.sub(r"\s+", " ", text).strip() #remove extra whitespace that occurs around apostrophes

        words = text.split()
        rmFront = {"at", "has", "is", "was", "are", "were", "liked", "be", "the", "a", "an", "thai", "pho", "jamaican", "chinese", 
                   "burger", "bread",  "mexican", "southern", "sandwiches", "gyro", "indian", "and", "or", ","}
        #above is a list of words to remove, will have to add more as time goes on
        while words and words[0].lower().strip(":") in rmFront: #get rid of leading words not part of the entity name
            words.pop(0)
        while words and words[0] == ":": 
            words.pop(0) #this is an edge case to remove colon from the front of the resturant name

        rmBack = {"has", "is", "was", "are", "were"}
        while words and words[-1].lower() in rmBack:
            words.pop()
        text = " ".join(words).strip() #gets all words back together 
        if len(text) < 2: #remove empty entities
            return ""
        extraWords = {"the", "a", "an", "and", "or", "but", "my", "our", "this", "that", "has", "is", "was", "are", "were", "been"} #going to need more of these
        if text.lower() in extraWords: #get rid of filler/ extra words that might throw google off
            return ""
        extraUpperWords = {"That's"} #extra edge case to catch uppercase words, will need to add more
        if text in extraUpperWords:
            return ""
        return text #return the entity back

    def _extract_locations(self, text: str): #extract the locations from text and return a list of all locations processed
        doc = self.nlp(text)

        locations = [] #store all cleaned locations from each input
        noDups = set() #set to store unique locations, may not need this
        for ent in doc.ents: #for all entites
            if (ent.label_ == "PLACE"): #get only places as it was the one picked in the custom patterns
                cleaned = self._clean_entity(ent.text)
                if cleaned and cleaned.lower() not in noDups:  
                    locations.append(cleaned) #add to list if cleaned
                    noDups.add(cleaned.lower()) #add to set in case of duplicates, also puts to lower to ensure that different spellings get checked
        return locations
    


def spaCy_full(text: str): #runs entire class
    entities = spaCyEntities()
    return entities._extract_locations(text) #returns list of all entities
