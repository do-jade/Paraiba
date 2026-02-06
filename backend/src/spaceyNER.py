import spacy
from spacy.pipeline import EntityRuler


def build_nlp():
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", after="ner", config={"overwrite_ents": True})

    patterns = [
        
        # Trigger verbs
        {"label": "PLACE", "pattern": [
            {"LOWER": {"IN": ["try","visit","visited","loved","love","ate","dined"]}},
            {"IS_TITLE": True, "OP": "+"}
        ]},

        # Category
        {"label": "PLACE", "pattern": [
            {"IS_TITLE": True, "OP": "+"},
            {"LOWER": {"IN": ["thai","pho","jamaican","chinese","burger","bread","mexican","southern","sandwiches","gyro", "pizza"]}},
        ]}
    ]

    cities = ["gainesville", "orlando", "miami"]
    ruler.add_patterns([
    {"label": "GPE", "pattern": [{"LOWER": city}]} for city in cities])
    

    ruler.add_patterns(patterns)
    return nlp

nlp = build_nlp()

text = """
If you are visiting Gainesville you need to go to Satchels pizza. Their hot honey one is good.
"""
doc = nlp(text)
print([(ent.text, ent.label_) for ent in doc.ents])
