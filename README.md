# Music Features Analyzer

## About the project

**Music Features Analyzer** is a backend Django application with integrated machine learning for audio data analysis and model training. It allows you to extract information about songs, detect genres, and analyze your music profile based on your Spotify top tracks.

## Architecture

The project consists of:

* Django backend API
* Machine learning module for audio analysis
* PostgreSQL database
* Docker containerized environment

## Tech stack

### Languages

* Python (backend and machine learning)
* JavaScript (UI/UX functionality)

### Technologies

* Docker (Dockerfile, docker-compose.yml)
* HTML/CSS (user interface)

## Features

* Audio feature extraction from music files
* Fetching user's top tracks from Spotify
* Spotify data analysis (returns your dominant genre)
* Statistics dashboard
* Live search (AJAX)

## How to use

1. Register and log in
2. Go to your profile page
3. Connect your Spotify account
4. Use one of the available features

## List of features

### Without Spotify

1. Audio feature extraction

### With Spotify

1. Load top tracks (render a page with all found tracks)
2. View genre prediction (returns your top genre)
3. Load user statistics

> [!IMPORTANT]
> You cannot add two identical songs to your profile unless they are different files.

## Example usage

### Feature carousel

<!-- ![Feature carousel](docs/gifs/carousel.gif) -->

### Audio upload

<!-- ![Audio upload](docs/gifs/upload.gif) -->

### Review audio features

<!-- ![Review audio features](docs/gifs/review.gif) -->

### Live search

<!-- ![Live search](docs/gifs/live-search.gif) -->

## License

This project is licensed under the MIT License.

## Future improvements

* Improve genre prediction accuracy
* Add a recommendation system
* Expand the analytics dashboard
