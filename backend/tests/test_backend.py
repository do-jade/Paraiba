#To run tests be in backend folder and run: py -3.12 -m pytest -v
#These are unit tests
import pytest
import re
from unittest.mock import MagicMock, patch, PropertyMock
# magic mock creates fake object, patch replaces code, propertymock mocks properties

@pytest.fixture(scope="module") #get module for spaCyNER and resusable for all tests
def ner():
    from spaCyNER import spaCyEntities
    return spaCyEntities()

class TestCleanEntity: 
    #tests for spaCyentities.clean_entity()

    @pytest.fixture(autouse=True) #fixture runs every test in its scope
    def setup(self):
        with patch("spaCyNER.spacy.load") as mock_load:#replaces with fake data
            mock_nlp = MagicMock()
            mock_load.return_value = mock_nlp.add_pipe.return_value = MagicMock()
            from spaCyNER import spaCyEntities
            self.ner = spaCyEntities() #initialize spacy for mock tests

    # --- Whitespace and unicode normalisation ---
 
    def test_removes_extra_whitespace(self): #ensure that clean entity removes white spaces
        assert self.ner.clean_entity("  Satchel's Pizza ") == "Satchel's Pizza"
 
    def test_single_quote(self): #quote normalization
        result = self.ner.clean_entity("Satchel\u2019s Pizza")
        assert "Satchel" in result
 
    def test_double_quotes(self): #double quote normalization
        result = self.ner.clean_entity("\u201cThe Venue\u201d")
        assert "The Venue" in result
 
    def test_left_single_quote(self): #just more quote normalization
        result = self.ner.clean_entity("Satchel\u2018s Pizza")
        assert "Satchel" in result
 
    def test_look_at_and_symbol(self): #ampersand issues I had
        result = self.ner.clean_entity("Burgers &amp; Brews")
        assert "&" in result
 
    def test_get_rid_of_spaces(self): # get rid of extra white space
        result = self.ner.clean_entity("Karma  Cream")
        assert result == "Karma Cream"
 
    def test_at(self): #test to remove at
        assert self.ner.clean_entity("at Dragonfly") == "Dragonfly"
 
    def test_ate(self): #test to remove ate
        assert self.ner.clean_entity("ate El Indio") == "El Indio"
 
    def test_went(self): #test to remove went
        assert self.ner.clean_entity("went Karma Cream") == "Karma Cream"
 
    def test_visited(self): #test to remove visited
        assert self.ner.clean_entity("visited Dragonfly") == "Dragonfly"
 
    def test_try(self): #test to remove try
        assert self.ner.clean_entity("try Satchel's") == "Satchel's"
 
    def test_tried(self): #test to remove tried
        assert self.ner.clean_entity("tried Green Papaya") == "Green Papaya"
 
    def test_loved(self): #test to remove loved
        assert self.ner.clean_entity("loved Karma Cream") == "Karma Cream"
 
    def test_about(self): #test to remove about
        assert self.ner.clean_entity("about Dragonfly") == "Dragonfly"
 
    def test_from(self): #ttest to remove from
        assert self.ner.clean_entity("from Dragonfly") == "Dragonfly"
 
    def test_cuisine_label(self): #keeps thai but ok
        result = self.ner.clean_entity("thai: Green Papaya")
        assert "Green Papaya" in result
 
    def test_comma(self): #test to remove commas
        assert self.ner.clean_entity(", Dragonfly") == "Dragonfly"
 
    def test_bullet(self): #test to remove period/bullet in list
        assert self.ner.clean_entity("· Dragonfly") == "Dragonfly"
 
    def test_dash(self): #test to remove dash
        assert self.ner.clean_entity("- Dragonfly") == "Dragonfly"
 
    def test_asterisk(self): #test to remove *
        assert self.ner.clean_entity("* Dragonfly") == "Dragonfly"
 
    def test_the(self): #test to remove the
        assert self.ner.clean_entity("the Venue") == "Venue"
 
    def test_is(self): #test to remove is
        assert self.ner.clean_entity("is Dragonfly") == "Dragonfly"
 
    def test_is_end(self): #test to remove is from end
        assert self.ner.clean_entity("Paper Bag Deli is") == "Paper Bag Deli"
 
    def test_was_end(self): #test to remove was from end
        assert self.ner.clean_entity("Venue was") == "Venue"
 
    def test_has_end(self): #test to reomve has from the end
        assert self.ner.clean_entity("Karma Cream has") == "Karma Cream"
 
    def test_are_end(self): #test to remove are from end
        assert self.ner.clean_entity("Tacos El Rancho are") == "Tacos El Rancho"
 
    def test_were_end(self): #test to remove were from end
        assert self.ner.clean_entity("Karma Cream were") == "Karma Cream"
 
    def test_which(self): #bigger trials
        result = self.ner.clean_entity("Dragonfly which is great")
        assert result == "Dragonfly"
 
    def test_that(self): #make sure no that
        result = self.ner.clean_entity("Satchel's that opened last year")
        assert result == "Satchel's"
 
    def test_because(self): #no bc
        result = self.ner.clean_entity("Karma Cream because it is sweet")
        assert result == "Karma Cream"
 
    def test_where(self): #no where
        result = self.ner.clean_entity("Dragonfly where we celebrated")
        assert result == "Dragonfly"

    def test_single_char(self): #no character entry
        assert self.ner.clean_entity("A") == ""
 
    def test_empty(self): #no return on empty string
        assert self.ner.clean_entity("") == ""
 
    def test_filler_word(self): #no filler words
        assert self.ner.clean_entity("the") == ""
 
    def test_filler_word_empty(self): #no title fillers
        assert self.ner.clean_entity("The") == ""
 
    def test_its(self): #no it's
        assert self.ner.clean_entity("It's") == ""
 
    def test_thats(self): #is allowed bc of single possisive restuarant names
        result = self.ner.clean_entity("That's")
        assert result == "That's"
 
    def test_lowercase_single_word(self): #no lowercase singles
        assert self.ner.clean_entity("pizza") == ""
 
    def test_all_caps(self): #no all caps with single word
        assert self.ner.clean_entity("BBQ") == ""
 
    def test_day_word(self): #no days of the week
        assert self.ner.clean_entity("Monday") == ""
 
    def test_cuisine_word(self): #no cuisine word by itself
        assert self.ner.clean_entity("Thai") == ""
 
    def test_gainesville(self): #no gainesville
        assert self.ner.clean_entity("Gainesville") == ""
 
    def test_xtra_stuff_food(self): #no extra foods
        assert self.ner.clean_entity("mexican food") == ""
 
    def test_random_phrases(self): #should not return on stuff like this
        assert self.ner.clean_entity("gas station") == ""
 
    def test_commons(self): #should not return anything near this
        result = self.ner.clean_entity("good food place restaurant")
        assert result == ""

    def test_normal_restaurant_name(self): #test for regular names
        assert self.ner.clean_entity("Dragonfly") == "Dragonfly"
 
    def test_possessive_name(self): #test for possessives
        assert self.ner.clean_entity("Satchel's Pizza") == "Satchel's Pizza"
 
    def test_multi_word_name(self): #test longer names
        assert self.ner.clean_entity("Hana Sushi Grill") == "Hana Sushi Grill"
 
    def test_name_with_ampersand(self): #test for &
        result = self.ner.clean_entity("Salt & Light")
        assert result == "Salt & Light"
 
    def test_name_with_connector(self): #test for connector words between names
        result = self.ner.clean_entity("Bistro de Paris")
        assert result == "Bistro de Paris"
 
    def test_possesive_word_name(self): #test for longer possesives
        result = self.ner.clean_entity("Pearl's Country Store BBQ")
        assert "Pearl" in result
 
 
class TestExtractLocations:
    #testing for extracting locations
 
    def _make_ent(self, text, label):
        ent = MagicMock()
        ent.text = text
        ent.label_ = label
        return ent
 
    def _build_ner_with_ents(self, ents):
        with patch("spaCyNER.spacy.load") as mock_load:
            mock_nlp = MagicMock()
            mock_load.return_value = mock_nlp
            mock_nlp.add_pipe.return_value = MagicMock()
            from spaCyNER import spaCyEntities
            instance = spaCyEntities()
        doc = MagicMock()
        doc.ents = ents
        instance.nlp = MagicMock(return_value=doc)
        return instance
 
    def test_returns_list(self): #test if the list returns
        ner = self._build_ner_with_ents([])
        result = ner.extract_locations("some text")
        assert isinstance(result, list)
 
    def test_single_place_entity(self): #test if the restuarant name is a place 
        ents = [self._make_ent("at Dragonfly", "PLACE")]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("I ate at Dragonfly yesterday")
        assert "Dragonfly" in result
 
    def test_non_place_labels_ignored(self): #test for gainesville as a GPE and name as a place
        ents = [
            self._make_ent("Gainesville", "GPE"),
            self._make_ent("at Satchel's", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("Gainesville has Satchel's")
        assert len(result) == 1
        assert result[0] == "Satchel's"
 
    def test_org_label_ignored(self): #test for org
        ents = [
            self._make_ent("University of Florida", "ORG"),
            self._make_ent("at Dragonfly", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("University of Florida is near Dragonfly")
        assert len(result) == 1
        assert result[0] == "Dragonfly"
 
    def test_person_label_ignored(self): #test for person
        ents = [
            self._make_ent("John Smith", "PERSON"),
            self._make_ent("at El Indio", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("John Smith ate at El Indio")
        assert len(result) == 1
 
    def test_deduplication(self): #see what happens with duplicates
        ents = [
            self._make_ent("at Dragonfly", "PLACE"),
            self._make_ent("at Dragonfly", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("Dragonfly is great. Dragonfly rules.")
        assert result.count("Dragonfly") == 1
 
    def test_case_insensitive_deduplication(self): #see what happens for duplicates with upper and lower names
        ents = [
            self._make_ent("at Dragonfly", "PLACE"),
            self._make_ent("at dragonfly", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("text")
        assert len(result) == 1
 
    def test_unicode_apostrophe_normalised(self): #test for unicode bc it is really annoying
        ents = [self._make_ent("at Satchel\u2019s Pizza", "PLACE")]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("I love Satchel\u2019s Pizza")
        assert len(result) == 1
        assert "Satchel" in result[0]
 
    def test_empty_text_returns_empty_list(self): #ensure empty list does not return anything
        ner = self._build_ner_with_ents([])
        assert ner.extract_locations("") == []
 
    def test_multiple_distinct_places(self): #make sure it actually works
        ents = [
            self._make_ent("at Dragonfly", "PLACE"),
            self._make_ent("at El Indio", "PLACE"),
            self._make_ent("visited Karma Cream", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("some text")
        assert len(result) == 3
 
    def test_filler_entities_excluded(self): #test similar things as above
        ents = [self._make_ent("the", "PLACE")]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("the")
        assert result == []
 
    def test_slash_is_spaced_before_nlp(self): #test if slashes do not exist
        ents = []
        ner = self._build_ner_with_ents(ents)
        ner.extract_locations("Burgers/Brews")
        call_args = ner.nlp.call_args[0][0]
        assert " / " in call_args
 
    def test_ampersand_entity_normalised_before_nlp(self): #test for ampersands given in some comments are not picked up
        ents = []
        ner = self._build_ner_with_ents(ents)
        ner.extract_locations("Salt &amp; Light")
        call_args = ner.nlp.call_args[0][0]
        assert "&amp;" not in call_args
 
    def test_cleaned_empty_entity_not_added(self): #test if cleaned entities are not added to list
        ents = [self._make_ent("Monday", "PLACE")]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("Monday")
        assert result == []
 
    def test_result_order_preserved(self): #test if order is preserved in a list
        ents = [
            self._make_ent("at Dragonfly", "PLACE"),
            self._make_ent("at El Indio", "PLACE"),
        ]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("text")
        assert result[0] == "Dragonfly"
        assert result[1] == "El Indio"
 
    def test_possessive_place_cleaned_correctly(self): #test if possesives are correctly processed
        ents = [self._make_ent("at Pearl's Country Store", "PLACE")]
        ner = self._build_ner_with_ents(ents)
        result = ner.extract_locations("I went to Pearl's Country Store")
        assert len(result) == 1
        assert "Pearl" in result[0]
 
 
class TestSpaCyFull:
    #bigger tests for spacy
 
    def test_returns_list(self): #test as an entire class for list
        with patch("spaCyNER.spaCyEntities") as MockClass:
            mock_instance = MagicMock()
            mock_instance.extract_locations.return_value = ["Dragonfly"]
            MockClass.return_value = mock_instance
            from spaCyNER import spaCy_full
            result = spaCy_full("I love Dragonfly")
            assert result == ["Dragonfly"]
 
    def test_creates_new_instance_each_call(self): #tests different instances of spacy
        with patch("spaCyNER.spaCyEntities") as MockClass:
            mock_instance = MagicMock()
            mock_instance.extract_locations.return_value = []
            MockClass.return_value = mock_instance
            from spaCyNER import spaCy_full
            spaCy_full("text one")
            spaCy_full("text two")
            assert MockClass.call_count == 2
 
    def test_passes_text_to_extract_locations(self): #test to check if text is getting passed down 
        with patch("spaCyNER.spaCyEntities") as MockClass:
            mock_instance = MagicMock()
            mock_instance.extract_locations.return_value = []
            MockClass.return_value = mock_instance
            from spaCyNER import spaCy_full
            spaCy_full("I ate at Karma Cream")
            mock_instance.extract_locations.assert_called_once_with("I ate at Karma Cream")
 
    def test_empty_text_returns_empty_list(self): #ensure empty list is not returned
        with patch("spaCyNER.spaCyEntities") as MockClass:
            mock_instance = MagicMock()
            mock_instance.extract_locations.return_value = []
            MockClass.return_value = mock_instance
            from spaCyNER import spaCy_full
            result = spaCy_full("")
            assert result == []
 
    def test_returns_multiple_locations(self): #just bigger test with more entities
        with patch("spaCyNER.spaCyEntities") as MockClass:
            mock_instance = MagicMock()
            mock_instance.extract_locations.return_value = ["Dragonfly", "El Indio"]
            MockClass.return_value = mock_instance
            from spaCyNER import spaCy_full
            result = spaCy_full("Dragonfly and El Indio are both great")
            assert len(result) == 2
 
 
#now switching to placeAPI
class TestGooglePlacesValidatorInit:
 
    def test_default_location_is_gainesville(self): #check for default location
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        assert v.default_location == "Gainesville, FL"
 
    def test_custom_location(self): #test if google takes a custom location other than default
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key", default_location="Orlando, FL")
        assert v.default_location == "Orlando, FL"
 
    def test_default_radius(self): #this is radius test for the geolocation
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        assert v.radius == 25000
 
    def test_custom_radius(self): #another test for location
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key", radius=10000)
        assert v.radius == 10000
 
    def test_api_key_stored(self): #ensure API is available
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("my-secret-key")
        assert v.api_key == "my-secret-key"
 
    def test_cache_starts_empty(self): #see what the cache is
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        assert v.cordsCache == {}
 
 
class TestGetCoordinates:
 
    @pytest.fixture
    def validator(self): #see if it can create itself
        from PlacesAPI import GooglePlacesValidator
        return GooglePlacesValidator("fake-key")
 
    def test_returns_lat_lon_tuple(self, validator): #this is to check lattitude and longitude of gainesville
        mock_result = MagicMock()
        mock_result.latitude = 29.6516
        mock_result.longitude = -82.3248
        validator.geocoder.geocode = MagicMock(return_value=mock_result)
        coords = validator.get_coordinates("Gainesville, FL")
        assert coords == (29.6516, -82.3248)
 
    def test_caches_result(self, validator): #see if geo caches the location
        mock_result = MagicMock()
        mock_result.latitude = 29.6516
        mock_result.longitude = -82.3248
        validator.geocoder.geocode = MagicMock(return_value=mock_result)
        validator.get_coordinates("Gainesville, FL")
        validator.get_coordinates("Gainesville, FL")
        assert validator.geocoder.geocode.call_count == 1
 
    def test_cache_returns_stored_value(self, validator): #see if geo caches and returns location
        validator.cordsCache["Gainesville, FL"] = (29.0, -82.0)
        validator.geocoder.geocode = MagicMock()
        result = validator.get_coordinates("Gainesville, FL")
        assert result == (29.0, -82.0)
        validator.geocoder.geocode.assert_not_called()
 
    def test_returns_none_when_geocode_fails(self, validator): #make sure that a place that doesnt exist returns None
        validator.geocoder.geocode = MagicMock(return_value=None)
        result = validator.get_coordinates("Unknown Place")
        assert result is None
 
    def test_returns_none_on_exception(self, validator): #if exception happens should return None
        validator.geocoder.geocode = MagicMock(side_effect=Exception("network error"))
        result = validator.get_coordinates("Gainesville, FL")
        assert result is None
 
    def test_different_locations_cached_separately(self, validator): #see if different locations are cached
        mock_gnv = MagicMock(latitude=29.65, longitude=-82.32)
        mock_orl = MagicMock(latitude=28.53, longitude=-81.37)
        validator.geocoder.geocode = MagicMock(side_effect=[mock_gnv, mock_orl])
        validator.get_coordinates("Gainesville, FL")
        validator.get_coordinates("Orlando, FL")
        assert "Gainesville, FL" in validator.cordsCache
        assert "Orlando, FL" in validator.cordsCache
 
 
class TestValidateLoc:
 
    @pytest.fixture
    def validator(self):
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        v.get_coordinates = MagicMock(return_value=(29.65, -82.32))
        return v
 
    def _mock_api(self, validator, place_id="ChIJabc123", place_name="Dragonfly", status="OK"): #mock API request to see if it gets it correct
        find_resp = MagicMock()
        find_resp.json.return_value = {
            "status": status,
            "candidates": [{"place_id": place_id}]
        }
        details_resp = MagicMock()
        details_resp.json.return_value = {
            "status": "OK",
            "result": {
                "name": place_name,
                "formatted_address": "1234 Main St, Gainesville, FL",
                "rating": 4.5,
                "user_ratings_total": 200,
                "types": ["restaurant", "food"],
                "editorial_summary": {"overview": "A great place"},
                "reviews": [{"text": "Loved it!"}],
                "serves_breakfast": False,
                "serves_brunch": False,
                "serves_lunch": True,
                "serves_dinner": True,
                "serves_beer": True,
                "serves_wine": False,
                "serves_vegetarian_food": True,
                "dine_in": True,
                "takeout": True,
                "delivery": False,
            }
        }
        return [find_resp, details_resp]
 
    def test_returns_dict_on_success(self, validator): #see if it will return the dictionary correctly
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            result = validator.validate_loc("Dragonfly")
        assert isinstance(result, dict)
 
    def test_dict_has_expected_keys(self, validator): #see if the dictionary stores all of the keys needed for mongo
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            result = validator.validate_loc("Dragonfly")
        expected_keys = {"name", "address", "rating", "review_count", "category",
                         "description", "googlereviews", "serves_breakfast",
                         "serves_brunch", "serves_lunch", "serves_dinner",
                         "serves_beer", "serves_wine", "serves_vegetarian",
                         "dine_in", "takeout", "delivery"}
        assert expected_keys.issubset(result.keys())
 
    def test_returns_correct_name(self, validator): #make sure it returns the right name
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            result = validator.validate_loc("Dragonfly")
        assert result["name"] == "Dragonfly"
 
    def test_returns_correct_rating(self, validator): #make sure it returns the correct rating
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            result = validator.validate_loc("Dragonfly")
        assert result["rating"] == 4.5
 
    def test_returns_correct_review_count(self, validator): #make sure it returns the right views
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            result = validator.validate_loc("Dragonfly")
        assert result["review_count"] == 200
 
    def test_returns_none_when_find_status_not_ok(self, validator): #make sure it returns an error if something goes wrong
        find_resp = MagicMock()
        find_resp.json.return_value = {"status": "ZERO_RESULTS", "candidates": []}
        with patch("requests.get", return_value=find_resp):
            result = validator.validate_loc("NonexistentPlace")
        assert result is None
 
    def test_returns_none_when_no_candidates(self, validator): #make sure it returns none when no candidates are returned
        find_resp = MagicMock()
        find_resp.json.return_value = {"status": "OK", "candidates": []}
        with patch("requests.get", return_value=find_resp):
            result = validator.validate_loc("MissingPlace")
        assert result is None
 
    def test_returns_none_when_name_mismatch(self, validator): #check if it returns none if names are different
        """If Google returns a totally different name, validate_loc should return None."""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator, place_name="Different Restaurant")
            result = validator.validate_loc("Dragonfly")
        assert result is None
 
    def test_uses_default_location_when_none_given(self, validator): #check if default location is given
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            validator.validate_loc("Dragonfly")
        validator.get_coordinates.assert_called_with("Gainesville, FL")
 
    def test_uses_custom_location_when_given(self, validator): #check if different location is given when not default
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator)
            validator.validate_loc("Dragonfly", location="Orlando, FL")
        validator.get_coordinates.assert_called_with("Orlando, FL")
 
    def test_returns_none_on_exception(self, validator): #make sure if exception happens it returns none
        with patch("requests.get", side_effect=Exception("connection timeout")):
            result = validator.validate_loc("Dragonfly")
        assert result is None
 
    def test_googlereviews_list_has_correct_length(self, validator): #test to see if google reviews are correct length
        find_resp = MagicMock()
        find_resp.json.return_value = {"status": "OK", "candidates": [{"place_id": "abc"}]}
        details_resp = MagicMock()
        details_resp.json.return_value = {
            "status": "OK",
            "result": {
                "name": "Dragonfly",
                "formatted_address": "123 St",
                "rating": 4.0,
                "user_ratings_total": 50,
                "types": ["restaurant"],
                "reviews": [{"text": f"Review {i}"} for i in range(3)],
            }
        }
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [find_resp, details_resp]
            result = validator.validate_loc("Dragonfly")
        assert result is not None
        assert len(result["googlereviews"]) == 3
 
    def test_googlereviews_capped_at_five(self, validator): #make sure google reviews only return top 5 results
        find_resp = MagicMock()
        find_resp.json.return_value = {"status": "OK", "candidates": [{"place_id": "abc"}]}
        details_resp = MagicMock()
        details_resp.json.return_value = {
            "status": "OK",
            "result": {
                "name": "Dragonfly",
                "formatted_address": "123 St",
                "rating": 4.0,
                "user_ratings_total": 50,
                "types": ["restaurant"],
                "reviews": [{"text": f"Review {i}"} for i in range(8)],
            }
        }
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [find_resp, details_resp]
            result = validator.validate_loc("Dragonfly")
        assert result is not None
        assert len(result["googlereviews"]) <= 5
 
    def test_description_none_when_no_editorial_summary(self, validator): #see if no description is available when no editorial summary is given
        find_resp = MagicMock()
        find_resp.json.return_value = {"status": "OK", "candidates": [{"place_id": "abc"}]}
        details_resp = MagicMock()
        details_resp.json.return_value = {
            "status": "OK",
            "result": {
                "name": "Dragonfly",
                "formatted_address": "123 St",
                "rating": 4.0,
                "user_ratings_total": 50,
                "types": ["restaurant"],
                "reviews": [],
            }
        }
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [find_resp, details_resp]
            result = validator.validate_loc("Dragonfly")
        assert result is not None
        assert result["description"] is None
 
    def test_partial_name_match_still_validates(self, validator): #see if names match when not fully given
        """'Pearl's Country Store' from spaCy should match "Pearl's Country Store and BBQ" on Google."""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = self._mock_api(validator, place_name="Pearl's Country Store and BBQ")
            result = validator.validate_loc("Pearl's Country Store")
        # ratio check uses max of forward/backward so this should pass
        assert result is not None
 
 
class TestValidateAllLocs:
 
    @pytest.fixture
    def validator(self):
        from PlacesAPI import GooglePlacesValidator
        v = GooglePlacesValidator("fake-key")
        return v
 
    def test_returns_list(self, validator): #make sure a list is returned
        validator.validate_loc = MagicMock(return_value=None)
        result = validator.validate_all_locs([])
        assert isinstance(result, list)
 
    def test_valid_entities_included(self, validator): #make sure that the right name is given as name
        mock_place = {"name": "Dragonfly", "rating": 4.5}
        validator.validate_loc = MagicMock(return_value=mock_place)
        result = validator.validate_all_locs(["Dragonfly"])
        assert len(result) == 1
        assert result[0]["name"] == "Dragonfly"
 
    def test_none_results_excluded(self, validator): #make sure that results that return None are excluded from the list
        validator.validate_loc = MagicMock(return_value=None)
        result = validator.validate_all_locs(["NonexistentPlace"])
        assert result == []
 
    def test_mixed_valid_and_invalid(self, validator): #bigger test if names are correctly returned when the are supposed to 
        def side_effect(entity):
            if entity == "Dragonfly":
                return {"name": "Dragonfly", "rating": 4.5}
            return None
        validator.validate_loc = MagicMock(side_effect=side_effect)
        result = validator.validate_all_locs(["Dragonfly", "FakePlace"])
        assert len(result) == 1
 
    def test_calls_validate_loc_for_each_entity(self, validator): #make sure the calls are correct
        validator.validate_loc = MagicMock(return_value=None)
        validator.validate_all_locs(["A", "B", "C"])
        assert validator.validate_loc.call_count == 3
 
    def test_empty_input_returns_empty_list(self, validator): #make sure that empty return means empty list
        validator.validate_loc = MagicMock()
        result = validator.validate_all_locs([])
        assert result == []
        validator.validate_loc.assert_not_called()
 
    def test_multiple_valid_results_all_returned(self, validator): #ensure that valid names are returned
        places = [{"name": f"Place{i}", "rating": 4.0} for i in range(3)]
        validator.validate_loc = MagicMock(side_effect=places)
        result = validator.validate_all_locs(["A", "B", "C"])
        assert len(result) == 3
 
 
class TestGoogleFull:
 
    def test_calls_validate_all_locs(self): #make sure validate all locs works
        with patch("PlacesAPI.GooglePlacesValidator") as MockClass:
            mock_instance = MagicMock()
            mock_instance.validate_all_locs.return_value = [{"name": "Dragonfly"}]
            MockClass.return_value = mock_instance
            from PlacesAPI import google_full
            result = google_full(["Dragonfly"], "fake-key")
        mock_instance.validate_all_locs.assert_called_once_with(["Dragonfly"])
 
    def test_passes_api_key(self): #make sure API key is passed in
        with patch("PlacesAPI.GooglePlacesValidator") as MockClass:
            mock_instance = MagicMock()
            mock_instance.validate_all_locs.return_value = []
            MockClass.return_value = mock_instance
            from PlacesAPI import google_full
            google_full(["Dragonfly"], "my-api-key")
        MockClass.assert_called_once_with("my-api-key", "Gainesville, FL", 25000)
 
    def test_passes_custom_location(self): #make sure custom locations are enabled
        with patch("PlacesAPI.GooglePlacesValidator") as MockClass:
            mock_instance = MagicMock()
            mock_instance.validate_all_locs.return_value = []
            MockClass.return_value = mock_instance
            from PlacesAPI import google_full
            google_full(["Dragonfly"], "key", location="Orlando, FL")
        MockClass.assert_called_once_with("key", "Orlando, FL", 25000)
 
    def test_passes_custom_radius(self): #make sure custom radius is enabled
        with patch("PlacesAPI.GooglePlacesValidator") as MockClass:
            mock_instance = MagicMock()
            mock_instance.validate_all_locs.return_value = []
            MockClass.return_value = mock_instance
            from PlacesAPI import google_full
            google_full(["Dragonfly"], "key", radius=5000)
        MockClass.assert_called_once_with("key", "Gainesville, FL", 5000)
 
    def test_returns_results(self): #make sure that results are actually returned
        with patch("PlacesAPI.GooglePlacesValidator") as MockClass:
            mock_instance = MagicMock()
            mock_instance.validate_all_locs.return_value = [{"name": "Dragonfly"}]
            MockClass.return_value = mock_instance
            from PlacesAPI import google_full
            result = google_full(["Dragonfly"], "key")
        assert result == [{"name": "Dragonfly"}]
 
 
 #switching to PariabaModel
class TestGetCategory:
    @pytest.fixture(autouse=True)
    def patch_imports(self):
        with patch("spaCyNER.spacy.load"), \
             patch("pymongo.MongoClient"), \
             patch("dotenv.load_dotenv"), \
             patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}):
            import sys
            sys.modules.pop("ParaibaModel", None)
            yield
 
    def _get_category(self): #make sure get category is correct
        import importlib
        import sys
        with patch("pymongo.MongoClient") as mock_client, \
             patch("dotenv.load_dotenv"), \
             patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}):
            mock_db = MagicMock()
            mock_client.return_value.__getitem__.return_value = mock_db
            mock_db.__getitem__.return_value.find.return_value = []
            mock_db.__getitem__.return_value.find_one.return_value = None
 
            sys.modules.pop("ParaibaModel", None)
            import ParaibaModel
            return ParaibaModel.getCategory
 
    def test_returns_general_when_no_match(self): #make sure that general is returned when no category matches
        getCategory = self._get_category()
        result = getCategory("Unnamed Place", None, [], [])
        assert result == ["general"]
 
    def test_returns_list(self): #make sure that a list returns
        getCategory = self._get_category()
        result = getCategory("Dragonfly Bar", None, [], [])
        assert isinstance(result, list)
 
    def test_detects_bbq_from_name(self): #checking for bbq as category
        getCategory = self._get_category()
        result = getCategory("Smokehouse BBQ", None, [], [])
        assert "bbq" in result
 
    def test_detects_pizza_from_name(self): #checking for italian as category
        getCategory = self._get_category()
        result = getCategory("Satchel's Pizza", None, [], [])
        assert "italian" in result
 
    def test_detects_sushi_from_name(self): #checking if japanese from category
        getCategory = self._get_category()
        result = getCategory("Hana Sushi Grill", None, [], [])
        assert "japanese" in result
 
    def test_detects_bar_from_google_type(self): #checking is bar from category
        getCategory = self._get_category()
        result = getCategory("Some Spot", None, [], ["bar"])
        assert "bar" in result
 
    def test_detects_cafe_from_google_type(self): #checking for cafe from category
        getCategory = self._get_category()
        result = getCategory("Morning Place", None, [], ["cafe"])
        assert "cafe" in result
 
    def test_detects_museum_from_google_type(self): #checking for museum from category
        getCategory = self._get_category()
        result = getCategory("Art Place", None, [], ["museum"])
        assert "museum" in result
 
    def test_detects_category_from_description(self): #checking for brewery from category
        getCategory = self._get_category()
        result = getCategory("Some Place", "Known for its craft beer on tap", [], [])
        assert "brewery" in result
 
    def test_for_hiking(self): #checking for outdoor only from category
        getCategory = self._get_category()
        result = getCategory("Paynes Prairie trail", None, [], [])
        assert "hiking" in result
 
    def test_adds_outdoor_tag_for_outdoor_category(self): #check if outdoor is also appended
        getCategory = self._get_category()
        result = getCategory("Paynes Prairie trail", None, [], [])
        assert "outdoor" in result
 
    def test_adds_indoor_tag(self): #check for indoor from category
        getCategory = self._get_category()
        result = getCategory("Dragonfly Bar Lounge", "cozy indoor cocktail bar", [], ["bar"])
        assert "indoor" in result
 
    def test_deduplicates_categories(self): #make sure it only returns one category for that type
        getCategory = self._get_category()
        result = getCategory("BBQ Smokehouse barbecue barbeque", None, [], [])
        assert result.count("bbq") == 1
 
    def test_detects_seafood_from_name(self): #check for seafood from category
        getCategory = self._get_category()
        result = getCategory("Larry's Seafood Shack", None, [], [])
        assert "seafood" in result
 
    def test_detects_burgers_from_name(self): #check for burgers from category
        getCategory = self._get_category()
        result = getCategory("Big Smash Burgers", None, [], [])
        assert "burgers" in result
 
    def test_detects_dessert_from_description(self): #check for dessert from category
        getCategory = self._get_category()
        result = getCategory("Sweet Stop", "Famous for their ice cream and desserts", [], [])
        assert "dessert" in result
 
    def test_review_threshold_single_review(self): #this tests if at least one review is needed
        getCategory = self._get_category()
        reviews = [{"text": "great ramen here"}]  # only 1 review
        result = getCategory("Mystery Place", None, reviews, [])
        assert "japanese" in result
 
    def test_review_threshold_two_reviews_needed(self): #with more than 3 reveiws needs at least two to match
        getCategory = self._get_category()
        reviews = [{"text": "great ramen"}] + [{"text": "no food mentioned"}] * 4
        result = getCategory("Mystery Place", None, reviews, [])
        # Only 1 of 5 reviews mentions ramen so should not be japanese
        assert "japanese" not in result
 
 
class TestMatchLocs:
 
    @pytest.fixture(autouse=True)
    def patch_imports(self):
        with patch("pymongo.MongoClient") as mock_client, \
             patch("dotenv.load_dotenv"), \
             patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}):
            mock_db = MagicMock()
            mock_client.return_value.__getitem__.return_value = mock_db
            mock_db.__getitem__.return_value.find.return_value = []
            import sys
            sys.modules.pop("ParaibaModel", None)
            yield
 
    def _get_match_locs(self):
        with patch("pymongo.MongoClient") as mock_client, \
             patch("dotenv.load_dotenv"), \
             patch.dict("os.environ", {"GOOGLE_API_KEY": "fake", "MONGODB_CONNECTION": "mongodb://fake"}):
            mock_db = MagicMock()
            mock_client.return_value.__getitem__.return_value = mock_db
            mock_db.__getitem__.return_value.find.return_value = []
            import sys
            sys.modules.pop("ParaibaModel", None)
            import ParaibaModel
            return ParaibaModel.matchLocs
 
    def test_exact_match(self): #test to make sure name matches
        matchLocs = self._get_match_locs()
        existing = {"dragonfly": {"name": "Dragonfly", "_id": "1"}}
        key, info = matchLocs("Dragonfly", existing)
        assert key == "dragonfly"
 
    def test_no_match_returns_none_tuple(self): #test to make sure None is in tuple if unknown
        matchLocs = self._get_match_locs()
        existing = {"karma cream": {"name": "Karma Cream", "_id": "2"}}
        key, info = matchLocs("Totally Unknown", existing)
        assert key is None
        assert info is None
 
    def test_single_word_overlap_matches(self): #test to see if overlapping words match
        matchLocs = self._get_match_locs()
        existing = {"satchel's pizza": {"name": "Satchel's Pizza", "_id": "3"}}
        key, info = matchLocs("Satchel's", existing)
        assert key == "satchel's pizza"
 
    def test_possessive_apostrophe_variants_match(self): #test about apostrophes, again a big issue I had
        matchLocs = self._get_match_locs()
        existing = {"pearl\u2019s country store": {"name": "Pearl\u2019s Country Store", "_id": "4"}}
        key, info = matchLocs("Pearl's Country Store", existing)
        assert key is not None
 
    def test_case_insensitive_exact_match(self): #test if uppercase does not matter
        matchLocs = self._get_match_locs()
        existing = {"dragonfly": {"name": "Dragonfly", "_id": "1"}}
        key, info = matchLocs("DRAGONFLY", existing)
        assert key == "dragonfly"
 
    def test_returns_correct_info_dict(self): #make sure it is returned the right info
        matchLocs = self._get_match_locs()
        info_data = {"name": "Karma Cream", "_id": "5"}
        existing = {"karma cream": info_data}
        key, info = matchLocs("Karma Cream", existing)
        assert info == info_data
 

@pytest.mark.integration
class TestIntegrationSpaCy:
 
    def test_went_to_pattern(self, ner): #make sure went to pattern worls
        result = ner.extract_locations("We went to Satchel's last night.")
        assert any("Satchel" in r for r in result)
 
    def test_at_pattern(self, ner): #make sure at works
        result = ner.extract_locations("Had lunch at El Indio today.")
        assert any("El Indio" in r for r in result)
 
    def test_possessive_spacy(self, ner): #make sure possessive works
        text = (
            "Pearl's Country Store and BBQ is incredible. "
            "It's attached to a gas station."
        )
        result = ner.extract_locations(text)
        assert any("Pearl" in r for r in result)
 
    def test_no_false_positives(self, ner): #make sure that it doesnt have filler words
        text = "The weather in Florida is really nice in spring."
        result = ner.extract_locations(text)
        for r in result:
            assert r.lower() not in {"the", "a", "an", "it", "is"}
 
    def test_multiple_locations_in_one_comment(self, ner): #test multiple locations from single comment
        text = "Try Satchel's for pizza and visit Dragonfly for cocktails."
        result = ner.extract_locations(text)
        assert len(result) >= 2
 
    def test_bullet_list_pattern(self, ner): #test on bulleted lists
        text = "My top picks:\n· Karma Cream\n· Dragonfly\n· El Indio"
        result = ner.extract_locations(text)
        assert len(result) >= 2
 
    def test_ampersand_name(self, ner): #test on &
        text = "Salt & Light is a great coffee shop."
        result = ner.extract_locations(text)
        assert any("Salt" in r for r in result)
 
    def test_possessive_short_name(self, ner): #test on one word names
        result = ner.extract_locations("We always go to Satchel's.")
        assert any("Satchel" in r for r in result)
 
    def test_extras(self, ner): #test if period triggers it
        result = ner.extract_locations("Visited Karma Cream yesterday.")
        assert any("Karma" in r for r in result)
  
    def test_no_locations_in_plain_sentence(self, ner): #test if no locations come up to see for false posititves
        text = "I was really hungry but could not decide what to eat."
        result = ner.extract_locations(text)
        for r in result:
            assert len(r) > 1