from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

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
    # Retrieves sentiment scores.
    scores = analyzer.polarity_scores(comment)
    
    print(f"Comment #{i}:")
    print(f"  Text: {comment}")
    print(f"  Negative: {scores['neg']:.3f}")
    print(f"  Neutral:  {scores['neu']:.3f}")
    print(f"  Positive: {scores['pos']:.3f}")
    print(f"  Compound: {scores['compound']:.3f}")
    
    # Classifies sentiment. 
    if scores['compound'] >= 0.05:
        sentiment_label = "Positive."

    elif scores['compound'] <= -0.05:
        sentiment_label = "Negative."

    else:
        sentiment_label = "Neutral."
    
    print(f"Classification: {sentiment_label}")
    print()
