from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

        # Added patterns geared towards attractions and restaurants. 
        self.positiveKeywords = [
            "hidden gem", "must try", "must-try", "go-to", "go to",
            "freshest", "fresh", "legit", "underrated", "secret", "worth",
            "winner", "been around forever", "local favorite",
            "authentic", "rec", "would recommend", "my pick", "top pick"
        ]

        self.negativeKeywords = [
            "fine", "okay", "only option",
            "nothing special", "overrated", "overhyped",
            "meh", "average", "mediocre", "not worth"
        ]

    def analyze(self, text):
        scores = self.vader.polarity_scores(text)
        compound = scores["compound"]
        textLower = text.lower()

        for keyword in self.positiveKeywords:
            if keyword in textLower:
                compound += 0.15

        for keyword in self.negativeKeywords:
            if keyword in textLower:
                compound -= 0.2

        compound = max(-1.0, min(1.0, compound))

        if compound >= 0.05:
            label = "Positive."

        elif compound <= -0.05:
            label = "Negative."

        else:
            label = "Neutral."

        return {
            "compound": round(compound, 3),
            "classification": label,
            "vaderCompound": round(scores["compound"], 3)
        }


def analyzer(texts): #input a comment to run entire vader program
    sentiment = SentimentAnalyzer() #call the class
    if isinstance(texts, str):
        return sentiment.analyze(texts) #only runs if one string
    if isinstance(texts, list) and len(texts) > 0: #if a list of strings
        scores = []
        for text in texts:
            result = sentiment.analyze(text)
            scores.append(result['compound']) #add the compound together
            avg_compound = sum(scores) / len(scores) #divide by the number of strings
            if avg_compound >= 0.05: #same logic as above but with compounded average
                label = "Positive"
            elif avg_compound <= -0.05:
                label = "Negative"
            else:
                label = "Neutral"
        return {
            "compound": round(avg_compound, 3),
            "classification": label,
            "vaderCompound": round(avg_compound, 3)  
        }
    return None
'''
# Same comments that Adam used for spaCy testing. 
sampleComments = [
    "Sushi Matsuri has some of the freshest sushi in town and has been around forever. That's my go-to spot.",
    "pho: the oxtail pho at Chopstix is legit, definitely the best in town.",
    "Thai: haven't been everywhere but Eim is the best I've had",
    "Jamaican: Tropical Eatz",
    "Satchel's pizza",
    "Chinese: Sohao is a mile above the other places for a full menu of authentic Chinese food.",
    "burger: DJ's Cast Iron Burgers",
    "bread: the sourdough at the Grove Street Market on Mondays",
    "south Indian: Indian Street Food is the only option and adequate",
    "Mexican: La Tienda is the clearcut winner for taqueria style.",
    "Southern: Underground Kitchen is pretty legit.",
    "Am I the only person not sold on Paper Bag Deli? I've tried 3 different sandwiches from there and all of them were meh, especially considering the price.",
    "My rec for sandwiches would be Hogans",
    "I liked Dominos, Pizza Hut, Satchel's Pizza, and Papa John's"
]

for i, comment in enumerate(sampleComments, 1):
    result = analyzer.analyze(comment)
    
    print(f"Comment #{i}:")
    print(f"  Text: {comment}")
    print(f"  VADER Compound:    {result['vaderCompound']:.3f}")
    print(f"  Enhanced Compound: {result['compound']:.3f}")
    print(f"  Classification: {result['classification']}")
    print()
'''