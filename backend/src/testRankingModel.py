import math
import pytest
from rankingModel import (
    redditScore,
    mlScore,
    googleScore,
    paraibaScore,
    scoreDestinations,
    mentionCeiling,
    upvoteCeiling,
    reviewCeiling,
)

# Reddit Score Section

class TestRedditScore:
    def test_zero_inputs_returns_zero(self):
        """No mentions and no upvotes should score 0."""
        assert redditScore(0, 0) == 0.0

    def test_output_bounded_above_by_one(self):
        """Score must never exceed 1.0."""
        assert redditScore(mentionCeiling, upvoteCeiling) <= 1.0

    def test_at_ceiling_returns_one(self):
        """Exactly at both ceilings should produce 1.0."""
        assert redditScore(mentionCeiling, upvoteCeiling) == 1.0

    def test_above_ceiling_capped_at_one(self):
        """Values above ceiling must be clamped, not overflow."""
        assert redditScore(mentionCeiling * 10, upvoteCeiling * 10) == 1.0

    def test_higher_mentions_gives_higher_score(self):
        """More mentions should always raise the score."""
        low = redditScore(1, 10)
        high = redditScore(10, 10)
        assert high > low

    def test_higher_upvotes_gives_higher_score(self):
        """More upvotes should always raise the score."""
        low = redditScore(5, 10)
        high = redditScore(5, 100)
        assert high > low

    def test_logarithmic_diminishing_returns(self):
        """Going from 1 to 10 mentions should help more than 40 to 50."""
        gain_early = redditScore(10, 0) - redditScore(1, 0)
        gain_late  = redditScore(50, 0) - redditScore(40, 0)
        assert gain_early > gain_late

    def test_returns_float_rounded_to_4_places(self):
        result = redditScore(5, 30)
        assert isinstance(result, float)
        assert result == round(result, 4)


# ML Score Section

class TestMlScore:
    def test_passthrough_of_sentiment(self):
        """mlScore should return the sentiment value rounded to 4 decimal places."""
        assert mlScore(0.7352) == 0.7352

    def test_zero_sentiment(self):
        assert mlScore(0.0) == 0.0

    def test_perfect_sentiment(self):
        assert mlScore(1.0) == 1.0

    def test_rounding(self):
        result = mlScore(0.123456789)
        assert result == round(0.123456789, 4)


# Google Score Section

class TestGoogleScore:
    def test_output_bounded_zero_to_one(self):
        """Google score must always be in [0, 1]."""
        assert 0.0 <= googleScore(1.0, 0) <= 1.0
        assert 0.0 <= googleScore(5.0, reviewCeiling * 5) <= 1.0

    def test_high_review_count_reduces_obscurity(self):
        """A place with many reviews should score lower than one with few."""
        score_hidden  = googleScore(4.5, 50)
        score_popular = googleScore(4.5, 900)
        assert score_hidden > score_popular

    def test_hidden_gem_bonus_applied(self):
        """Reviews over 500 and rating > 4.5 should earn the bonus."""
        with_bonus    = googleScore(4.6, 400)
        without_bonus = googleScore(4.4, 400)   
        assert with_bonus > without_bonus

    def test_hidden_gem_bonus_not_applied_above_threshold(self):
        """Reviews less than or equal to 500 should NOT trigger the bonus even with a great rating."""
        at_threshold  = googleScore(4.6, 500)   
        just_under    = googleScore(4.6, 499)   
        assert just_under > at_threshold

    def test_perfect_obscure_gem_capped_at_one(self):
        """A 5 star place with 0 reviews and the bonus score must not exceed 1.0."""
        assert googleScore(5.0, 0) <= 1.0

    def test_higher_rating_gives_higher_score(self):
        """With identical review counts, higher rating should win."""
        assert googleScore(4.8, 300) > googleScore(4.0, 300)

    def test_zero_reviews_max_obscurity(self):
        """A brand-new place with no reviews should get full obscurity credit."""
        score = googleScore(4.0, 0)
        expected_obscurity = 1.0
        expected = (0.60 * (4.0 / 5.0)) + (0.40 * expected_obscurity)
        assert score == pytest.approx(expected, abs=0.001)

    def test_at_review_ceiling_obscurity_is_zero(self):
        """Exactly at the review ceiling, obscurity contribution is 0."""
        score = googleScore(4.0, reviewCeiling)
        expected = 0.60 * (4.0 / 5.0) 
        assert score == pytest.approx(expected, abs=0.001)


# Paraíba Score Section

class TestParaibaScore:
    def test_returns_expected_keys(self):
        result = paraibaScore(4.5, 300, 5, 40.0, 0.7)
        assert set(result.keys()) == {"Paraíba Score", "Reddit Score", "ML Score", "Google Score"}

    def test_final_score_range(self):
        """Final score should be on a 0 to 100 scale."""
        result = paraibaScore(4.5, 300, 5, 40.0, 0.7)
        assert 0 <= result["Paraíba Score"] <= 100

    def test_zero_everything_gives_low_score(self):
        """Reddit and sentiment are 0, but obscurity is maxed, which the score should reflect that."""
        result = paraibaScore(0.0, 0, 0, 0.0, 0.0)
        assert result["Paraíba Score"] < 25   
        assert result["Reddit Score"] == 0.0
        assert result["ML Score"] == 0.0

    def test_component_scores_consistent_with_final(self):
        """Manually verify the weighted sum matches the reported final score."""
        r = paraibaScore(4.6, 400, 3, 50.0, 0.75)
        expected = round(
            (0.40 * r["Reddit Score"] +
             0.20 * r["ML Score"] +
             0.40 * r["Google Score"]) * 100,
            2
        )
        assert r["Paraíba Score"] == pytest.approx(expected, abs=0.01)

    def test_better_inputs_give_higher_score(self):
        """A clearly stronger restaurant should outscore a weaker one."""
        strong = paraibaScore(4.9, 100, 20, 80.0, 0.95)
        weak   = paraibaScore(3.0, 900, 1,   2.0, 0.10)
        assert strong["Paraíba Score"] > weak["Paraíba Score"]

    def test_zero_sentiment_penalizes_score(self):
        """Identical restaurants except sentiment = 0 should score lower."""
        with_sentiment    = paraibaScore(4.5, 300, 5, 40.0, 0.8)
        without_sentiment = paraibaScore(4.5, 300, 5, 40.0, 0.0)
        assert with_sentiment["Paraíba Score"] > without_sentiment["Paraíba Score"]


# Destination Score Section

class TestScoreDestinations:
    BASE = {
        "name": "Test Place",
        "googleRating": 4.5,
        "googleReviews": 300,
        "redditMentions": 5,
        "averageUpvotes": 40.0,
        "sentimentScore": 0.7,
    }

    def test_sorted_descending(self):
        """Results must be sorted highest Paraíba Score first."""
        destinations = [
            {**self.BASE, "name": "Low",  "googleRating": 2.0, "sentimentScore": 0.0},
            {**self.BASE, "name": "High", "googleRating": 4.9, "sentimentScore": 0.9},
            {**self.BASE, "name": "Mid",  "googleRating": 3.5, "sentimentScore": 0.5},
        ]
        results = scoreDestinations(destinations)
        scores = [r["Score Result"]["Paraíba Score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_missing_key_produces_zero_score(self):
        """A destination missing a required field should get score 0.0, not crash."""
        bad = {"name": "Broken Place", "googleRating": 4.5}
        results = scoreDestinations([bad])
        assert results[0]["Score Result"]["Paraíba Score"] == 0.0
        assert "error" in results[0]["Score Result"]

    def test_empty_list_returns_empty(self):
        assert scoreDestinations([]) == []

    def test_single_destination_returned(self):
        results = scoreDestinations([self.BASE])
        assert len(results) == 1
        assert "Score Result" in results[0]

    def test_original_fields_preserved(self):
        """All original destination fields should still be present in output."""
        results = scoreDestinations([self.BASE])
        for key in self.BASE:
            assert key in results[0]
