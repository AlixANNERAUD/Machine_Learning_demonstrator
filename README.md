# Machine Learning Demonstrator

## Introduction

Exploit musical data to demonstrate machine learning techniques, mainly classification and clustering.
The final product is a web application that allows users to provide some information about their music preferences and get recommendations based on the data.

## Dependencies

- Python
- Django
- NumPy
- Pandas
- Scikit-learn
- Spotipy

Install the dependencies using the following command:

```bash 
pip install -r requirements.txt
```

## Usage

To run the web application, use the following command:

```bash
python manage.py runserver
```

## Key features

- [ ] Use user's data (authentication required)
- [ ] Use a public playlist

- [ ] Visualization of musical data
  - [ ] Provide multiple visualization options for user's musical data
  - [ ] Provide multiple other summarization options (artists, playlist, etc.)
- [ ] Recommendation system
  - [ ] Provide multiple recommendation options (mood, genre, etc.)
  - [ ] Constraint-based recommendation (known artists, speed, etc.)
  - [ ] Prompt-base recommendation (LLM)
- [ ] Playlist generation
  - [ ] Provide multiple playlist generation options (mood, genre, etc.)
  - [ ] Constraint-based playlist generation (known artists, speed, etc.)
  - [ ] Prompt-base playlist generation (LLM)

## Methods

- [x] Query musical data from Spotify API
- [ ] Clustering of musical data
- [ ] Classification of musical data
- [ ] PCA and t-SNE for dimensionality reduction

- [ ] Extract musical features from raw audio files
- [ ] Fourier transform

- [ ] Extract linguistic features from lyrics

- [ ] Django web application
