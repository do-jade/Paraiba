# Paraiba
Senior Project for UF by Adam Popovich, Dohyun Lee, Jimin Kwak, and Thomas Hewatt

##Dependencies

This project is implemented in Python and  JavaScript and requires the following libraries.

### Backend (Python)

- **Python 3.12.x**
    Later versions are not compatible with current spaCy library

- **spaCy (3.7.x)**  
  Used for natural language processing, including tokenization, sentence segmentation, and rule-based named entity recognition to extract candidate place names from Reddit discussions.

- **VADER Sentiment**  
  VADER is used to estimate the sentiment polarity of sentences or clauses mentioning extracted places.

- **RapidFuzz**  
  A string matching library used to normalize and merge variants of place names like punctuation differences.

- **NumPy (< 2.0)**  
  Required by spaCy and related NLP components. The version is constrained to maintain compatibility with spaCy’s current release.

All Python dependencies are pinned and managed via `pyproject.toml`.

To install backend dependencies:

```bash
pip install .
python -m spacy download en_core_web_sm