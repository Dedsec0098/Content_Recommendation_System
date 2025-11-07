# 🎬 Movie Recommender System

A content-based movie recommendation system built with Python, Streamlit, and TMDB API. Deployed using Docker for easy containerization.

## Features

- ✅ Content-based movie recommendations using cosine similarity
- ✅ Movie posters from TMDB API
- ✅ YouTube trailer links
- ✅ Interactive Streamlit web interface
- ✅ Dockerized for easy deployment
- ✅ 4800+ movies database

## Tech Stack

- **Backend**: Python, Pandas, NumPy, Scikit-learn, NLTK
- **Frontend**: Streamlit
- **API**: TMDB (The Movie Database)
- **Containerization**: Docker, Docker Compose
- **Machine Learning**: Bag of Words, Cosine Similarity

## Prerequisites

- Docker and Docker Compose installed
- OR Python 3.11+ (for local development)

## 🐳 Running with Docker (Recommended)

### Option 1: Using Docker Compose (Easiest)

```bash
# Build and start the container
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The app will be available at: **http://localhost:8501**

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t movie-recommender .

# Run the container
docker run -p 8501:8501 movie-recommender

# Run in detached mode
docker run -d -p 8501:8501 --name movie-app movie-recommender

# Stop the container
docker stop movie-app
docker rm movie-app
```

## 💻 Running Locally (Without Docker)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at **http://localhost:8501**

## 📁 Project Structure

```
recomender_system/
├── app.py                      # Main Streamlit application
├── movies.pkl                  # Preprocessed movie data
├── similarity.pkl              # Similarity matrix
├── tmdb_5000_movies.csv       # Raw movie dataset
├── tmdb_5000_credits.csv      # Raw credits dataset
├── recomender_system.ipynb    # Model training notebook
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── .dockerignore              # Docker ignore file
└── README.md                   # This file
```

## 🎯 How It Works

1. **Data Processing**: Movies are processed using NLP techniques (stemming, bag of words)
2. **Feature Extraction**: Extracts genres, keywords, cast, crew, and overview
3. **Vectorization**: Converts text features into numerical vectors
4. **Similarity Calculation**: Uses cosine similarity to find similar movies
5. **Recommendation**: Returns top 5 most similar movies with posters and trailers

## 🚀 Usage

1. Open the app in your browser
2. Select a movie from the dropdown
3. Click "Show Recommendation"
4. View 5 similar movies with:
   - Movie posters
   - Watch Trailer buttons (opens YouTube)

## 🔧 Configuration

### Environment Variables

You can customize the Streamlit configuration by setting these environment variables:

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### TMDB API Key

The app uses TMDB API for fetching posters and trailers. The API key is currently hardcoded in `app.py`. For production:

1. Get your API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Replace the API key in `app.py` or use environment variables

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs

# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Missing Posters/Trailers

Some movies might not have posters or trailers due to:
- Movie ID mismatch with TMDB database
- Movie removed from TMDB
- Network issues
- API rate limits

The recommendations will still work correctly.

## 📊 Dataset

- **Source**: TMDB 5000 Movie Dataset
- **Movies**: ~4800 movies
- **Features**: genres, keywords, cast, crew, overview

## 🔮 Future Enhancements

- [ ] User authentication
- [ ] Save favorite movies
- [ ] Collaborative filtering
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Add movie ratings and reviews
- [ ] Real-time search with autocomplete
- [ ] Mobile responsive design

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ using Python, Streamlit, and Docker

---

⭐ If you find this project useful, please consider giving it a star!
