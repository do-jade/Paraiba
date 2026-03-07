# python -m spacy download en_core_web_lg

import re #regex for cleaning up entities
import spacy #import spacy NER

class spaCyEntities:
    def __init__(self):
        self.nlp = self.build_nlp() #initialize nlp with custom patterns below

    def build_nlp(self): #set the patterns and build nlp pipeline
        nlp = spacy.load("en_core_web_lg") #load the pre-trained large English semantic model
        ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True}) #entity ruler allows for custom patterns to be used
        #the patterns are ran before the natural entity processing spaCy does and the patterns will overwrite what spaCy gives
        #basically want to ensure that all locations and restuarants are labeled as places to be picked up later

        placeEnders = [ #Names of places with these at the end
            "bbq", "grill", "grille", "kitchen", "market", "deli", "cafe", "café",
            "store", "pizza", "sushi", "thai", "bistro", "bar", "house", "shack",
            "boil", "wings", "burgers", "tacos", "eatery", "donuts", "bakery",
            "cream", "spice", "garden", "gardens", "ramen", "poke", "pocha", "momo",
            "seafood", "steaks", "sandwich", "sandwiches", "bagels", "cheesesteaks",
            "barbeque", "barbecue", "noodles", "winery", "brewery", "lounge", "diner",
            "truck", "station", "park", "preserve", "trail", "zoo", "co.", "co",
            "farm", "skatepark", "springs", "wetlands", "forest", "overlook"
        ]

        beforeTriggers = [ #words before place name that trigger it
            "try", "tried", "visit", "visited", "love", "loved", "like", "liked",
            "ate", "dined", "recommend", "recommending", "about", "from", "called"
        ]

        # Strict connectors — only prepositions/articles, NOT "and" (too greedy)
        betweenWords = ["of", "de", "du", "el", "le", "les", "di", "del", "von", "van", "n", "by"]

        capitalized = r"^[A-Z][A-Za-z]+$" #Captitalized words
        anyCapitalizedWord = r"^[A-Z][A-Za-z]*$" #Capitalized words that are broken

        #above are for matching with Spacy bc it does a bad job

        patterns = [ #custom patterns created specifically to pick up restuarants and attractions
            #possesive names
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": r"^[A-Z][A-Za-z]{1,}(\u2019s|'s|'s|')?$"}},
                {"TEXT": {"IN": ["\u2019s", "'s", "'s", "'"]}, "OP": "?"},
                {"TEXT": {"REGEX": capitalized}, "OP": "*"}
            ]},

            # names with &
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": anyCapitalizedWord}},
                {"TEXT": {"IN": ["&", "&amp;"]}},
                {"TEXT": {"REGEX": anyCapitalizedWord}},
                {"TEXT": {"REGEX": capitalized}, "OP": "*"}
            ]},

            # Both sides must be single capitalized words with the word "and" between them
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"LOWER": "and"},
                {"TEXT": {"REGEX": capitalized}}
            ]},

            # amepersand with no spaces
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": r"^[A-Z](&[A-Z])+$"}},
                {"TEXT": {"REGEX": capitalized}, "OP": "*"},
                {"LOWER": {"IN": placeEnders}, "OP": "?"}
            ]},

            # capitalized word with any of the place enders above
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": anyCapitalizedWord}, "OP": "+"},
                {"LOWER": {"IN": placeEnders}}
            ]},

            # Capitalized word with a place ender eventually
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": r"^[a-z]+$"}, "OP": "?"},
                {"LOWER": {"IN": placeEnders}}
            ]},

            # Words in that trigger location names
            {"label": "PLACE", "pattern": [
                {"LOWER": {"IN": beforeTriggers}},
                {"TEXT": {"REGEX": capitalized}, "OP": "+"}
            ]},

            # At a place
            {"label": "PLACE", "pattern": [
                {"LOWER": "at"},
                {"TEXT": {"REGEX": capitalized}, "OP": "+"}
            ]},

            # Go/went to place
            {"label": "PLACE", "pattern": [
                {"LOWER": {"IN": ["go", "went"]}},
                {"LOWER": "to"},
                {"TEXT": {"REGEX": capitalized}, "OP": "+"}
            ]},

            # location is/was/has
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}, "OP": "+"},
                {"LOWER": {"IN": ["is", "was", "has"]}}
            ]},

            # list separated by commas
            {"label": "PLACE", "pattern": [
                {"TEXT": ","},
                {"TEXT": {"REGEX": capitalized}, "OP": "+"}
            ]},

            # list separated by commas but with lowercase names
            {"label": "PLACE", "pattern": [
                {"TEXT": ","},
                {"TEXT": {"REGEX": r"^[a-z][a-z]+$"}},
                {"LOWER": {"IN": placeEnders}, "OP": "?"}
            ]},

            # bullets and dashed lists
            {"label": "PLACE", "pattern": [
                {"TEXT": {"IN": ["·", "-", "*", "\u2013", "\u2022"]}},
                {"TEXT": {"REGEX": capitalized}, "OP": "+"}
            ]},

            # Two consecutive capitalized words
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}}
            ]},

            # capitatlized plus connectors plus capitalized
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"LOWER": {"IN": betweenWords}},
                {"TEXT": {"REGEX": capitalized}}
            ]},

            # Three consecutive captialized words
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}}
            ]},

            # Four captitalized words
            {"label": "PLACE", "pattern": [
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}},
                {"TEXT": {"REGEX": capitalized}}
            ]},
        ]

        ruler.add_patterns(patterns) #load all patterns to entity ruler
        return nlp #return the nlp object with custom patterns added in

    def clean_entity(self, text: str):
        text = text.replace("\u2019", "'").replace("\u2018", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        text = text.replace("&amp;", "&")
        # Strip words with *, -, " "
        text = re.sub(r"^\*+", "", text)
        text = re.sub(r"^-+", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        words = text.split()

        rmFront = { #list of words to remove, will have to add more as time goes on
            "at", "has", "is", "was", "are", "were", "liked", "loved", "like",
            "be", "the", "a", "an", "try", "tried", "visit", "visited", "ate",
            "went", "to", "about", "from", "for", "and", "or", ",", "·", "-", "*",
            "–", "•", "recommend", "inside", "called", "it's", "its", "also",
            "formerly", "but", "while", "across", "big"
        }
        while words and words[0].lower().strip(":,·*–•-") in rmFront: #Remove the extra characters
            words.pop(0)
        while words and words[0] in {"·", "-", "*", "–", "•", ","}: #remove more extra characters
            words.pop(0)

        rmBack = {"has", "is", "was", "are", "were", "where"} #remove words from back of extracted locations
        while words and words[-1].lower() in rmBack: #pop the words not needed
            words.pop()

        wordSplit = {"where", "which", "that", "who", "because", "since", #words that show two different sides
                       "although", "though", "unless", "until", "while"}
        for i, w in enumerate(words):
            if w.lower() in wordSplit:
                words = words[:i]
                break

        text = " ".join(words).strip() #join after taking these words out

        if len(text) < 2:
            return "" #Do not return if less than 2 chars

        beginWords = { #remove these words that commonly show up in the beginning of the location name
            "not", "so", "my", "best", "honestly", "although", "definitely",
            "they", "the", "this", "that", "those", "these", "there", "then",
            "we", "you", "he", "she", "it", "i", "and", "but", "or", "also",
            "just", "never", "most", "some", "any", "all", "no", "yes", "if",
            "when", "where", "how", "what", "who", "why", "as", "with",
            "good", "great", "very", "really", "probably", "plus", "does",
            "everyone", "everything", "anyone", "nothing", "edit", "new",
            "def", "giant", "unassuming", "authentic", "tons", "la", "hmm",
            "two", "people", "take", "hey", "beef", "cash", "brunch", "watching",
            "only", "check", "none", "maybe", "smash", "thicker", "consistent",
            "stir", "oddly", "congratulations", "last", "again", "reviews",
            "hopefully", "lesser", "tasty", "small", "their", "oh", "might",
            "second", "jazz", "here", "both", "big", "never", "oops",
            "rosemary", "gouda", "veggie", "chimichurri", "scallop", "tuna",
        }

        dayWords = { #remove dayWords of the week, they are generally capitalized
            "monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday", "tuesdayWords", "sundayWords", "mondayWords",
        }

        cuisneWords = { #remove most cuisine words
            "thai", "korean", "chinese", "mexican", "italian", "indian",
            "african", "caribbean", "egyptian", "vietnamese", "cambodian",
            "mediterranean", "japanese", "american", "southern", "cajun",
            "french", "spanish", "greek", "turkish", "ethiopian",
        }

        generals = { #remove generic words found throught the current comments DB
            "university", "main", "street", "avenue", "road", "boulevard",
            "lane", "way", "court", "place", "north", "south", "east", "west",
            "downtown", "uptown", "alachua", "micanopy", "newberry",
            "gainesville", "ocala", "williston", 
            "tower", "archer", "tractor", "supply", "ave", "st", "rd",
             "rec", "parks", "city", "facebook", 
            "hawthorne", "duval", "buffalo", "falafel", "tex",
            "asian", "ting", "shake", "chicken", "burrito",
        }

        xtraStuffFound = { #These are things that wont get out so far
            # food descriptors
            "mexican food", "chinese food", "korean food", "caribbean food",
            "italian food", "egyptian food", "african cuisine", "cambodian food",
            "indian cuisine", "thai food", "great mexican food", "best burgers",
            "good food", "tasty food", "good italian food", "great mexican",
            "cajun vietnamese", "good italian", "love indian cuisine",
            # dishes not restaurants
            "coco bread", "double wrapped", "not just pizza",
            "chimichurri sandwich", "scallop burrito", "tuna pesto melt",
            "everything bagel", "bulgogi omlette", "tofu fish sandwich",
            "augusta chicken sandwich", "calabrian wings", "their monte cristo",
            "le croque", "carribbean spice spicy beef patty", "burrito brothers primo beef burrito",
            # generic phrases
            "motor city", "outdoor bbq", "south american", "best cheese steaks",
            "gas station", "convenience store", "taco truck", "ave food park",
            "tractor supply", "sirloin steaks", "korean barbeque",
            "it was formerly", "not gnv", "fried chicken sandwich",
            "dog gone good diner", "so good", "university and main",
            "tower and archer", "tienda and boca", "vietnamese and thai",
            "thai and i", "city of gainesville", "parks & rec", "parks and rec",
            "giant amazing deli", "wetlands preserve", "high springs", "miccanopy",
            "newberry rd", "millhopper plaza", "mexican eatery",
            "daybreakgnv", "monsieur", "tex mex", "tex-mex",
        }

        if text.lower() in xtraStuffFound: #return empty if it is in the extra set
            return ""

        #for below it does not return the things above as well as lowercase words or word length less than 4 (This may be a miskate)
        if len(text.split()) == 1:
            if text.lower() in beginWords: 
                return ""
            if text.lower() in dayWords:
                return ""
            if text.lower() in cuisneWords:
                return ""
            if text.lower() in generals:
                return ""
            if text.islower():
                return ""
            if text.isupper() and len(text) <= 4:
                return ""

        commonWords = { #common words to get rid of
            "the", "a", "an", "and", "or", "of", "in", "on", "at", "to",
            "for", "with", "my", "their", "is", "are", "was", "were", "has",
            "food", "place", "restaurant", "best", "good", "great", "amazing",
            "authentic", "fresh", "quality", "portions", "most", "ever", "how",
            "worth", "drive", "certainly", "underrated", "incredible", "all",
            "about", "but", "does", "hold", "candle", "can", "see", "some",
            "pretty", "cool", "wildlife", "like", "deer", "gators", "sorts",
            "free", "nature", "parks", "get", "smoked", "sausage", "daily",
            "specials", "puts", "together", "tasty", "hole", "wall", "chain",
            "restaurants", "than", "more", "from", "been", "spectacular", "just",
            "not", "only", "pizza", "sandwich", "burrito", "melt", "bagel",
        }
        word_list = text.split()
        if len(word_list) > 2: #This removes these words from the list
            common_count = sum(1 for w in word_list if w.lower() in commonWords)
            if common_count / len(word_list) > 0.4:
                return ""

        return text

    def extract_locations(self, text: str): #extract the locations from text and return a list of all locations processed
        text = re.sub(r"/", " / ", text) #replace " "
        text = text.replace("&amp;", "&") #replace amersands
        #below are to clean the text because spacy cannot get them correct for whatever reason
        text = (text
                .replace("\u2019", "'").replace("\u2018", "'") 
                .replace("\u201c", '"').replace("\u201d", '"'))

        doc = self.nlp(text) #load in text from Mongo

        locations = [] #stored all cleaned locations
        noDups = set() #set to store unique locations, may not need this

        for ent in doc.ents: #for all entites
            if (ent.label_ == "PLACE"): #get only places as it was the one picked in the custom patterns
                cleaned = self.clean_entity(ent.text)
                if cleaned and cleaned.lower() not in noDups:  
                    locations.append(cleaned) #add to list if cleaned
                    noDups.add(cleaned.lower()) #add to set in case of duplicates, also puts to lower to ensure that different spellings get checked
        return locations


def spaCy_full(text: str): #runs entire class
    entities = spaCyEntities()
    return entities.extract_locations(text) #runs list of all entities
