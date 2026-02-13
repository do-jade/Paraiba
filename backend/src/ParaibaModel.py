from spaCyNER import spaCy_full
from PlacesAPI import google_full
from dotenv import load_dotenv
#need to place in dependencies dotenv
import os


load_dotenv()
googleAPI = os.getenv('GOOGLE_API_KEY')

textFull = """
Sushi Matsuri has some of the freshest sushi in town and has been around forever. That's my go-to spot.
pho: the oxtail pho at Chopstix is legit, definitely the best in town.
Thai: haven't been everywhere but Eim is the best I've had
Jamaican: Tropical Eatz
Satchel's pizza
Chinese: Sohao is a mile above the other places for a full menu of authentic Chinese food.
burger: DJ's Cast Iron Burgers
bread: the sourdough at the Grove Street Market on Mondays
south Indian: Indian Street Food is the only option and adequate
Mexican: La Tienda is the clearcut winner for taqueria style.
Southern: Underground Kitchen is pretty legit.
Am I the only person not sold on Paper Bag Deli? I've tried 3 different sandwiches from there and all of them were meh, especially considering the price.
My rec for sandwiches would be Hogans
I liked Dominos, Pizza Hut, Satchel's Pizza, and Papa John's
""" #just for testing rn


locations = spaCy_full(textFull) #calls spacy ner
print("This is the entities returned by spaCy:")
for location in locations:
    print(f" {location}")
defaultLocation = "Gainesville, FL" #not needed by why not
validatedLocations = google_full(locations, googleAPI ,defaultLocation) #calls places api with entities from spaCy