#To run tests be in backend folder and run: py -3.12 -m pytest -v
#These are integration and system tests
import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId #allows for mongoDB to pass in object ID
import sys

def full_google_example(name="Dragonfly", rating=4.5, review_count=200): #example with Dragonfly and filled out return from Google Places API
    return {
        "name": name,
        "address": "123 Main St, Gainesville, FL",
        "rating": rating,
        "review_count": review_count,
        "category": ["restaurant", "food"],
        "description": f"A great spot called {name}",
        "googlereviews": [{"text": "Loved it!"}],
        "serves_breakfast": False, "serves_brunch": False,
        "serves_lunch": True,  "serves_dinner": True,
        "serves_beer": True,   "serves_wine": False,
        "serves_vegetarian": True, "dine_in": True,
        "takeout": True, "delivery": False,
    }


def paraiba_module(): #import the ParaibaModel class with all of the connections patched out. No mongo and no google api key
    sys.modules.pop("ParaibaModel", None)
    with patch("pymongo.MongoClient") as mock_client, \
         patch("dotenv.load_dotenv"), \
         patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}):
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value.find.return_value = [] #returns an empty object but gets the functionality at the end. 
        import ParaibaModel
        return ParaibaModel


def run_pipeline(comments, existing_paraibas, spacy_entities, google_results, #helper to pass in a Reddit comment similar to what MongoDB, also takes in fake data for entities
                  vader_result=None, paraiba_score=None): #google results, vader, and paraiba
    sys.modules.pop("ParaibaModel", None) #fresh import everytime

    with patch("pymongo.MongoClient") as mock_client, \
         patch("dotenv.load_dotenv"), \
         patch.dict("os.environ", {"GOOGLE_API_KEY": "fake-key", "MONGODB_CONNECTION": "mongodb://fake"}), \
         patch("spaCyNER.spaCyEntities") as MockSpacy, \
         patch("PlacesAPI.GooglePlacesValidator") as MockGoogle, \
         patch("vader.analyzer") as mock_vader, \
         patch("rankingModel.paraibaScore") as mock_score:
        #replaces dependancies with fake data. Fake db connection, fake env, fake API, no real spacy model, no http call to goodle, no sentiment or pariaba scores
        mock_db = MagicMock() #fake mongo
        mock_client.return_value.__getitem__.return_value = mock_db #returns test client
        mock_reddit_col, mock_paraiba_col = MagicMock(), MagicMock() 
        mock_db.__getitem__.side_effect = lambda n: mock_reddit_col if n == "comments" else mock_paraiba_col #gets an item from mock comments collection
        mock_reddit_col.find.return_value = comments #returns the fake comments passed in
        mock_paraiba_col.find.return_value = [
            {"name": n, "_id": f"id_{i}"} for i, n in enumerate(existing_paraibas)
        ] #empty list with no locations left, find comments and docs passed in

        spacy_instance = MagicMock()
        MockSpacy.return_value = spacy_instance
        spacy_instance.extract_locations.side_effect = [
            spacy_entities.get(c["comment_text"], []) for c in comments
        ] #controls what spacy finds in each comment, callls extract locations on each item

        google_instance = MagicMock() #control what Places API returns
        MockGoogle.return_value = google_instance
        google_instance.validate_all_locs.return_value = google_results #returns fake entries of entities placed in

        mock_vader.return_value = vader_result or {"compound": 0.5} #fake vader
        mock_score.return_value = {"Paraíba Score": paraiba_score or 72.0} #fake pariaba

        import ParaibaModel  #triggers pipeline at module level

        return mock_paraiba_col, mock_reddit_col #returns what calls would have been made to mongoDB


def fake_comment(text, upvotes=5, cid="c1", link="https://reddit.com/r/GNV/1"):
    return {"_id": cid, "comment_text": text, "upvotes": upvotes,
            "link": link, "processed": False} #This is just to make a fake comment in the format of mongoDB


#below are integration tests
@pytest.mark.integration
class TestSpaCyToPlacesIntegration: #testing from spacy to places API integration

    @pytest.fixture(scope="class")
    def ner(self): #creating ner pipeline and setting it up
        from spaCyNER import spaCyEntities
        return spaCyEntities()

    def test_spacy_output_is_valid_input_for_places(self, ner): #every spacy entity must be nonempty 
        entities = ner.extract_locations("We went to Satchel's last night.")
        assert len(entities) >= 1
        for entity in entities:
            assert isinstance(entity, str) and len(entity) > 0

    def test_spacy_entities_forwarded_to_validate_all_locs(self, ner): #Test to see if validate locs calls more than once
        comment = "Try Satchel's for pizza and visit Dragonfly for cocktails."
        entities = ner.extract_locations(comment)
        assert len(entities) >= 2
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key") #pass in fake key
        v.validate_loc = MagicMock(return_value=None)
        v.validate_all_locs(entities) #pass in entities
        assert v.validate_loc.call_count == len(entities) #see if the call is the same as the length of entities passed in

    def test_places_result_has_all_keys_paraiba_needs(self, ner): #validate locs must have all necessary information and keys
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        v.validate_loc = MagicMock(return_value= full_google_example("Karma Cream"))
        results = v.validate_all_locs(["Karma Cream"])
        required = {"name", "address", "rating", "review_count", "category",
                    "description", "googlereviews", "serves_breakfast", "serves_brunch",
                    "serves_lunch", "serves_dinner", "serves_beer", "serves_wine",
                    "serves_vegetarian", "dine_in", "takeout", "delivery"}
        assert required.issubset(results[0].keys()) #make sure all keys are there that are required

    def test_bad_spacy_entities_silently_skipped(self, ner): #ensure that empty lists do not crash and non entity names are skipped
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        v.validate_loc = MagicMock(return_value=None)
        assert v.validate_all_locs(["definitely", "good food", ""]) == []


@pytest.mark.integration
class TestSpaCyToCategoryAndMatchLocs: #spacy to category and match location work without network
    
    @pytest.fixture(scope="class")
    def ner(self):
        from spaCyNER import spaCyEntities
        return spaCyEntities()

    @pytest.fixture(scope="class")
    def paraiba(self): #returns the correct module
        return paraiba_module()

    @pytest.mark.parametrize("comment,name_hint,description,expected_category", [
        ("Satchel's Pizza is the best.", "Satchel", "Wood-fired pizza", "italian"),
        ("Pearl's Country Store and BBQ is incredible.", "Pearl", "Smoked brisket", "bbq"),
    ]) #these are to get the right entity and information
    def test_spacy_name_flows_to_correct_category(self, ner, paraiba,comment, name_hint, description, expected_category): #name should get the right category
        entities = ner.extract_locations(comment) #get the names out of the comment
        name = next((e for e in entities if name_hint in e), None)
        assert name is not None, f"spaCy did not extract a name containing '{name_hint}'" #get name
        assert expected_category in paraiba.getCategory(name, description, [], ["restaurant"]) #make sure categories match

    def test_outdoor_trail_gets_outdoor_tag(self, ner, paraiba): #test of outdoor tag
        entities = ner.extract_locations("The Sweetwater Wetlands trail is beautiful.") #comment
        name = next((e for e in entities if "Sweetwater" in e or "Wetlands" in e),
                    "Sweetwater Wetlands trail")
        result = paraiba.getCategory(name, None, [], [])
        assert "outdoor" in result or any(c in result for c in ("hiking", "park", "water body")) #make sure the categories are correct

    def test_known_location_matched_by_matchlocs(self, ner, paraiba): #test to see if known entity gets updated
        existing = {"satchel's pizza": {"name": "Satchel's Pizza", "_id": "abc"}} #this is an existing entry
        entities = ner.extract_locations("We always go to Satchel's Pizza on Friday.")
        satchels = next((e for e in entities if "Satchel" in e), None)
        assert satchels is not None
        key, _ = paraiba.matchLocs(satchels, existing)
        assert key == "satchel's pizza" #make sure everything matches

    def test_apostrophe_variant_matched_by_matchlocs(self, ner, paraiba): #test for different apostrophe types
        existing = {"pearl\u2019s country store": {"name": "Pearl\u2019s Country Store", "_id": "p1"}}
        entities = ner.extract_locations("Pearl's Country Store and BBQ is attached to a gas station.")
        pearl = next((e for e in entities if "Pearl" in e), None)
        if pearl:
            key, _ = paraiba.matchLocs(pearl, existing)
            assert key is not None

#Now for the system tests
@pytest.mark.system
class TestNewLocationPipeline:
   #These tests are for all integrated files all in pariaba model including placesAPI, rankingModel, spacyNER, and vader

    def test_new_location_triggers_upsert_with_upsert_true(self): #new entity should only have one call
        comment = fake_comment("I love Dragonfly, best cocktail bar in town.", upvotes=10)
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment["comment_text"]: ["Dragonfly"]},
            google_results=[ full_google_example("Dragonfly")],
        )
        paraiba_col.update_one.assert_called_once()
        assert paraiba_col.update_one.call_args[1].get("upsert") is True

    def test_upsert_document_has_required_fields(self): #test that every field is there
        comment = fake_comment("Dragonfly is the best bar.", upvotes=15)
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment["comment_text"]: ["Dragonfly"]},
            google_results=[ full_google_example("Dragonfly", rating=4.7)],
        )
        doc = paraiba_col.update_one.call_args[0][1]["$setOnInsert"]
        required = {"address", "rating", "reviewCount", "sentimentRating", "ranking",
                    "upvotes", "mentionCount", "comments", "googleReviews",
                    "link", "categoryType", "location"}
        assert required.issubset(doc.keys()), f"Missing: {required - doc.keys()}"

    def test_upsert_filter_uses_google_name_and_values_are_correct(self): #filter must use google, comments, google comments, description, and name to check
        comment = fake_comment("El Indio is great.", upvotes=10,
                                link="https://reddit.com/test")
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment["comment_text"]: ["El Indio"]},
            google_results=[ full_google_example("El Indio", rating=4.3)],
            vader_result={"compound": 0.85},
            paraiba_score=88.5,
        )
        assert paraiba_col.update_one.call_args[0][0] == {"name": "El Indio"} #look at name
        doc = paraiba_col.update_one.call_args[0][1]["$setOnInsert"] #this is mongo call
        assert doc["rating"] == 4.3
        assert doc["upvotes"] == 10
        assert doc["sentimentRating"] == 0.85
        assert doc["ranking"] == 88.5
        assert doc["location"] == "Gainesville, FL"
        assert "https://reddit.com/test" in doc["link"] #make sure the right information is getting pulled out

    def test_mention_count_and_upvotes_aggregate_across_comments(self): #test to make sure mentioncount and upvotes are beign properly handled
        comments = [
            fake_comment("Dragonfly is great.", upvotes=10, cid="c1", link="https://r/1"),
            fake_comment("Dragonfly is great.", upvotes=20, cid="c2", link="https://r/2"),
            fake_comment("Dragonfly is great.", upvotes=5,  cid="c3", link="https://r/3"),
        ]
        entities_map = {c["comment_text"]: ["Dragonfly"] for c in comments}
        paraiba_col, _ = run_pipeline(
            comments=comments, existing_paraibas=[],
            spacy_entities=entities_map,
            google_results=[ full_google_example("Dragonfly")],
        )
        doc = paraiba_col.update_one.call_args[0][1]["$setOnInsert"]
        assert doc["mentionCount"] == 3 #three mentions mean mention count of 3
        assert doc["upvotes"] == 35 #these are the correct upvotes

    def test_reddit_comment_marked_processed_and_no_entity_skips_write(self): #make sure comments are marked when processed and empty comments are skipped
        good = fake_comment("Dragonfly is my favourite.", upvotes=7, cid="c1") #this is a correct comment
        empty = fake_comment("The weather is nice today.", upvotes=2, cid="c2") #this comment has no name to be pulled out

        paraiba_col, reddit_col = run_pipeline(
            comments=[good, empty], existing_paraibas=[],
            spacy_entities={
                good["comment_text"]: ["Dragonfly"],
                empty["comment_text"]: [],
            },
            google_results=[ full_google_example("Dragonfly")], #get goole results
        )
        # Only comments with entities get marked processed 
        # empty comments are skipped
        processed_ids = [c.args[0]["_id"] for c in reddit_col.update_one.call_args_list]
        assert "c1" in processed_ids
        assert "c2" not in processed_ids
        # only one call to mongo
        paraiba_col.update_one.assert_called_once()

    def test_multiple_locations_in_one_comment_both_upserted(self): #test to see if two names come up then it creates two different entities
        text = "Try Satchel's and Dragonfly this weekend."
        comment = fake_comment(text, upvotes=6)
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={text: ["Satchel's Pizza", "Dragonfly"]},
            google_results=[ full_google_example("Satchel's Pizza"),  full_google_example("Dragonfly")],
        )
        assert paraiba_col.update_one.call_count == 2

    def test_google_finding_nothing_skips_upsert(self): #test to see if there are no returned google results then no call to Mongo
        comment = fake_comment("I ate at SomeFakePlace.", upvotes=1)
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment["comment_text"]: ["SomeFakePlace"]},
            google_results=[],
        )
        paraiba_col.update_one.assert_not_called()


@pytest.mark.system
class TestExistingLocationPipeline: #test to make sure that existing entities are updated properly when new entities are added

    def existing_doc(self, name="Dragonfly", mention_count=3): #existing location 
        return {
            "name": name, "_id": ObjectId(),
            "mentionCount": mention_count, "rating": 4.5,
            "reviewCount": 200, "comments": [{"text": "Old comment"}],
        }

    def update_it(self, new_comments, existing_doc, vader_result=None, paraiba_score=None): #updating the location with all of the correct return results
        sys.modules.pop("ParaibaModel", None)
        existing_name = existing_doc["name"]

        with patch("pymongo.MongoClient") as mock_client, \
             patch("dotenv.load_dotenv"), \
             patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}), \
             patch("spaCyNER.spaCyEntities") as MockSpacy, \
             patch("PlacesAPI.GooglePlacesValidator") as MockGoogle, \
             patch("vader.analyzer") as mock_vader, \
             patch("rankingModel.paraibaScore") as mock_score:

            mock_db = MagicMock()
            mock_client.return_value.__getitem__.return_value = mock_db
            mock_reddit_col, mock_paraiba_col = MagicMock(), MagicMock()
            mock_db.__getitem__.side_effect = lambda n: mock_reddit_col if n == "comments" else mock_paraiba_col
            mock_reddit_col.find.return_value = new_comments
            mock_paraiba_col.find.return_value = [{"name": existing_name, "_id": existing_doc["_id"]}]
            mock_paraiba_col.find_one.return_value = existing_doc

            spacy_instance = MagicMock()
            MockSpacy.return_value = spacy_instance
            spacy_instance.extract_locations.side_effect = [[existing_name] for _ in new_comments]

            MockGoogle.return_value.validate_all_locs.return_value = []
            mock_vader.return_value = vader_result or {"compound": 0.6}
            mock_score.return_value = {"Paraíba Score": paraiba_score or 75.0}

            import ParaibaModel  # noqa
            return mock_paraiba_col

    def test_update_uses_inc_push_and_set(self): #test to make sure the correct mongo calls are being called
        existing = self.existing_doc()
        new_comments = [
            fake_comment("Dragonfly is still great.", upvotes=7, cid=f"c{i}")
            for i in range(2)
        ]
        paraiba_col = self.update_it(new_comments, existing,
                                       vader_result={"compound": 0.77},
                                       paraiba_score=91.0)

        all_calls = paraiba_col.update_one.call_args_list
        inc_call  = next((c for c in all_calls if "$inc"  in c[0][1]), None)
        push_call = next((c for c in all_calls if "$push" in c[0][1]), None)
        set_call  = next((c for c in all_calls if "$set"  in c[0][1]), None)

        assert inc_call  is not None, "$inc not found"
        assert push_call is not None, "$push not found"
        assert set_call  is not None, "$set not found"

        assert inc_call[0][1]["$inc"]["mentionCount"] == 2 #make sure that it is getting updated in Mongo
        assert set_call[0][1]["$set"]["sentimentRating"] == 0.77
        assert set_call[0][1]["$set"]["ranking"] == 91.0


@pytest.mark.system
class TestAcceptanceCriteria: #testing for bigger scenarios
    @pytest.mark.parametrize("comment_text,upvotes,google_name,check_field,expected", [
        ("Dragonfly is incredible.", 99, "Dragonfly", "upvotes", 99),# upvotes stored correctly
        ("Karma Cream is a hidden gem.", 20, "Karma Cream", "location", "Gainesville, FL"), # location always Gainesville
    ])
    def test_scalar_fields_stored_correctly(self, comment_text, upvotes,
                                            google_name, check_field, expected):
        comment = fake_comment(comment_text, upvotes=upvotes)
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment_text: [google_name]},
            google_results=[ full_google_example(google_name)],
        )
        doc = paraiba_col.update_one.call_args[0][1]["$setOnInsert"] #ensure everything is set correctly on insert
        assert doc[check_field] == expected

    def test_complete_document_written_with_all_required_fields(self): # when a comment gets processed then the document has all of the correct fields
        comment = fake_comment("Satchel's Pizza is the best.", upvotes=42,
                                link="https://reddit.com/acceptance")
        paraiba_col, _ = run_pipeline(
            comments=[comment], existing_paraibas=[],
            spacy_entities={comment["comment_text"]: ["Satchel's Pizza"]},
            google_results=[ full_google_example("Satchel's Pizza", rating=4.8)],
        )
        doc = paraiba_col.update_one.call_args[0][1]["$setOnInsert"]
        assert doc is not None
        for field in ("rating", "sentimentRating", "ranking", "upvotes",
                      "mentionCount", "link", "categoryType", "comments"):
            assert field in doc, f"'{field}' missing from document"
        assert isinstance(doc["categoryType"], list) and len(doc["categoryType"]) >= 1
        stored_texts = [c["text"] for c in doc.get("comments", [])]
        assert comment["comment_text"] in stored_texts
        assert "https://reddit.com/acceptance" in doc["link"]